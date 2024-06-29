# 作   者：林枭熠
# 开发时间:2024/6/15 下午5:49
from django.db import transaction
from ninja import Query
from ninja_extra import api_controller, ControllerBase, route, exceptions, status
from ninja_extra.ordering import Ordering, ordering
from ninja_extra.pagination import (
    paginate, PageNumberPaginationExtra, PaginatedResponseSchema
)
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from api.forum.Filter import PostFilterSchema, PostCommentFilterSchema
from api.forum.models import PostInfo, PostTag, PostComment, PostFavor
from api.forum.schema import PostSchemaListOut, PostSchemaDetailOut, PostCreateUpdateSchemaIn, \
    PostCommentCreateUpdateSchemaOne, PostCommentSchemaOut, PostFavorDetailedSchemaOut, PostFavorOwnedListSchemaOut
from PIL import Image

@api_controller("/forum/posts", tags=["posts"])
class PostController(ControllerBase):
    """
    用于帖子管理的API控制器，get方法无权限认证，但其它方法需要登录认证，操作自己的帖子
    """

    @route.get(
        '',
        response=PaginatedResponseSchema[PostSchemaListOut],
        url_name="get-posts-list",
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['create_time', 'click_num', 'favor_num', 'comment_num'])
    def list_posts(self, filters: Query[PostFilterSchema]):
        """
        获取帖子列表，并进行排序和分页，无权限认证，搜索字段：['search', 'author', 'tag', 'is_hot', "is_new"]

        search：帖子标题名称title、简介brief_content搜索

        author：帖子作者的用户名username模糊搜索

        tag：梯子标签名name模糊搜索

        is_hot：是否热门商品，Q(click_num__gt=10) | Q(favor_num__gt=5) |  Q(comment_num__gt=3)

        is_new：是否新品，创建帖子时间在3天内的帖子
        """
        Posts = PostInfo.objects.all()
        Posts = filters.filter(Posts)
        return Posts

    @route.get(
        "/{uuid:post_id}",
        response=PostSchemaDetailOut,
        url_name="get-one-post-detail"
    )
    def retrieve_post(self, post_id: str):
        """
        输入帖子id，获取帖子详情，并更新点击数，无权限认证
        """
        post = self.get_object_or_exception(
            PostInfo.objects.all(),
            id=post_id,
            error_message=f"id为 {post_id} 的帖子不存在",
        )
        # 商品点击数+1
        post.click_num += 1
        post.save()
        return post

    @route.post(
        "create/{str:tag_name}",
        response={201: PostSchemaDetailOut, 400: dict},
        url_name="create-post",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def create_post(self, post_schema: PostCreateUpdateSchemaIn, tag_name: str):
        """
        新建帖子，需要登录认证限，输入帖子信息，返回帖子详情
        """
        tag_instance = self.get_object_or_exception(
            PostTag.objects.all(),
            name=tag_name,
            error_message=f"名字为 {tag_name} 的帖子标签不存在",
        )
        # 如果有封面图片
        print(self.context.request.FILES)
        if "front_image" in self.context.request.FILES and self.context.request.FILES["front_image"] is not None:
            front_image = self.context.request.FILES["front_image"]
            # 确保上传的是图片
            try:
                Image.open(front_image).verify()
            except Exception as e:
                return 400, {"message": "上传的封面图片格式不正确"}
            user = self.context.request.user
            # 医生用户帖子数+1
            if user.is_doctor:
                user.doctor_info.post_num += 1
                user.doctor_info.save()
            post_instance = post_schema.create_post(author=user, tag=tag_instance, front_image=front_image)
            return 201, post_instance
        else:
            user = self.context.request.user
            # 医生用户帖子数+1
            if user.is_doctor:
                user.doctor_info.post_num += 1
                user.doctor_info.save()
            post_instance = post_schema.create_post(author=user, tag=tag_instance)
            return 201, post_instance

    @route.put(
        "/update/{uuid:post_id}",
        response={200: PostSchemaDetailOut},
        url_name="update-post",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def update_post(self, post_id: str, post_schema: PostCreateUpdateSchemaIn):
        """
        更新帖子，只能更新用户发的，且需要用户自身权限
        """
        post_instance = self.get_object_or_exception(
            PostInfo.objects.all(),
            id=post_id,
            error_message=f"id为 {post_id} 的帖子不存在",
        )
        if post_instance.author != self.context.request.user:
            raise exceptions.PermissionDenied("只能更新自己的帖子")
        post = post_schema.update_post(post_instance)
        return 200, post

    @route.delete(
        "/delete/{uuid:post_id}",
        url_name="delete-post",
        response={204: dict},
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def delete_post(self, post_id: str):
        """
        删除帖子，需要用户自身权限
        """
        post_instance = self.get_object_or_exception(
            PostInfo.objects.all(),
            id=post_id,
            error_message=f"id为 {post_id} 的帖子不存在",
        )
        if post_instance.author != self.context.request.user:
            raise exceptions.PermissionDenied("只能删除自己的帖子")
        user = self.context.request.user
        if user.is_doctor:
            user.doctor_info.post_num -= 1
            user.doctor_info.save()
        post_instance.delete()
        return self.create_response("帖子成功删除", status_code=status.HTTP_204_NO_CONTENT)

    @route.put(
        "/favor/{uuid:post_id}",
        response={201: PostFavorDetailedSchemaOut, 204: None},
        url_name="add-post-to-favor",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def favor_post(self, post_id: str):
        """
        添加帖子到点赞列表，或者取消点赞，有权限认证，需要登录
        """
        user = self.context.request.user
        post = self.get_object_or_exception(
            PostInfo.objects.all(),
            id=post_id,
            error_message=f"id为 {post_id} 的帖子不存在",
        )
        exists = PostFavor.objects.filter(post=post, user=user).exists()
        # 未点赞，创建点赞记录，点赞数+1
        if not exists:
            post.favor_num += 1
            post.save()
            return 201, PostFavor.objects.create(post=post, user=user)
        # 已点赞，删除点赞记录，点赞数-1
        else:
            post.favor_num -= 1
            post.save()
            favor = PostFavor.objects.get(post=post, user=user)
            favor.delete()
            return self.create_response("点赞已取消", status_code=status.HTTP_204_NO_CONTENT)

    @route.get(
        '/favor',
        response=PaginatedResponseSchema[PostFavorOwnedListSchemaOut],
        url_name="get-user's-post-favor-list",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['create_time', 'post__favor_num', 'post__create_time', 'post__modify_time'])
    def list_post_favors(self):
        """
        获取用户的点赞列表，有权限认证，需要登录，只能访问自己的点赞列表
        """
        favor_queryset = PostFavor.objects.filter(user=self.context.request.user)
        return favor_queryset


@api_controller("/forum/posts/comment", tags=["post_comments"])
class PostCommentController(ControllerBase):
    """
    用于帖子评论管理的API控制器，get方法无权限认证，但其它方法需要登录认证，操作自己的帖子留言
    """

    @route.get(
        '',
        response=PaginatedResponseSchema[PostCommentSchemaOut],
        url_name="get-post_comments-list",
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['create_time', 'modify_time'])
    def list_post_comments(self, filters: Query[PostCommentFilterSchema]):
        """
        获取帖子评论列表，并进行排序和分页，无权限认证，搜索字段：["post_id", "user_id", "user_username"]

        post_id：帖子id

        user_id：用户id

        user_username：用户用户名
        """
        PostsComment = PostComment.objects.all()
        PostsComment = filters.filter(PostsComment)
        return PostsComment

    @route.post(
        "create/{uuid:post_id}",
        response={201: PostCommentSchemaOut},
        url_name="create-post_comment",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def create_post_comment(self, post_comment_schema:  PostCommentCreateUpdateSchemaOne, post_id: str):
        """
        新建帖子评论，需要登录认证限，输入帖子id，和评论信息，返回帖子评论详情
        """
        post_instance = self.get_object_or_exception(
            PostInfo.objects.all(),
            id=post_id,
            error_message=f"id为 {post_id} 的帖子不存在",
        )
        post_instance.comment_num += 1
        post_instance.save()
        user = self.context.request.user
        post_comment_instance = post_comment_schema.create_post_comment(user=user, post=post_instance)
        return 201, post_comment_instance

    @route.put(
        "/update/{uuid:post_comment_id}",
        response={200: PostCommentSchemaOut},
        url_name="update-post_comment",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def update_post_comment(self, post_comment_id: str, post_comment_schema: PostCommentCreateUpdateSchemaOne):
        """
        更新帖子评论，只能更新用户发的，且需要用户自身权限
        """
        post_comment_instance = self.get_object_or_exception(
            PostComment.objects.all(),
            id=post_comment_id,
            error_message=f"id为 {post_comment_id} 的帖子评论不存在",
        )
        if post_comment_instance.user != self.context.request.user:
            raise exceptions.PermissionDenied("只能更新自己的帖子评论")
        post_comment = post_comment_schema.update_post_comment(post_comment_instance)
        return 200, post_comment

    @route.delete(
        "/delete/{uuid:post_comment_id}",
        url_name="delete-post_comment",
        response={204: dict},
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def delete_post(self, post_comment_id: str):
        """
        删除帖子评论，需要用户自身权限
        """
        post_comment_instance = self.get_object_or_exception(
            PostComment.objects.all(),
            id=post_comment_id,
            error_message=f"id为 {post_comment_id} 的帖子评论不存在",
        )
        if post_comment_instance.user != self.context.request.user:
            raise exceptions.PermissionDenied("只能更新自己的帖子评论")
        post_comment_instance.delete()
        return self.create_response("帖子评论成功删除", status_code=status.HTTP_204_NO_CONTENT)
