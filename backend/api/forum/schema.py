# 作   者：林枭熠
# 开发时间:2024/6/15 下午5:50
from typing import Type, Any

from ninja_extra import service_resolver
from ninja_extra.controllers import RouteContext
from ninja_schema import ModelSchema
from pydantic import field_validator

from api.forum.models import PostTag, PostInfo, PostFavor, PostComment
from api.users.schema import UserNameSchema, UserRetrieveOutSchema


class PostTagSchema(ModelSchema):
    """
    用于返回帖子标签序列化展示
    """

    class Config:
        model = PostTag
        include = "__all__"


class PostCreateUpdateSchemaIn(ModelSchema):
    """
    用于创建修改帖子详细信息序列化展示
    """

    class Config:
        model = PostInfo
        include = ["title", "brief_content", "content"]
        optional = ["brief_content"]

    # 创建帖子
    def create_post(self, **kwargs: Any) -> Type[PostInfo]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return PostInfo.objects.create(**_data)

    # 更新帖子
    def update_post(self, instance: Any, **kwargs: Any) -> Any:
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PostSchemaListOut(ModelSchema):
    """
    用于返回帖子列表序列化展示，不包含帖子内容，用户信息只给id、name
    """
    tag: PostTagSchema
    author: UserNameSchema

    @field_validator("front_image")
    def front_image_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        return context.request.build_absolute_uri(value_data)

    class Config:
        model = PostInfo
        exclude = ["content"]
        optional_field = "front_image"


class PostSchemaDetailOut(ModelSchema):
    """
    用于返回帖子详情序列化展示，包含帖子内容，用户信息只给id、name
    """
    tag: PostTagSchema
    author: UserNameSchema

    @field_validator("front_image")
    def front_image_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        return context.request.build_absolute_uri(value_data)

    class Config:
        model = PostInfo
        include = "__all__"
        optional_field = "front_image"


class PostFavorDetailedSchemaOut(ModelSchema):
    """
    用于点赞详情返回的schema
    """
    post: PostSchemaListOut
    user: UserRetrieveOutSchema

    class Config:
        model = PostFavor
        include = ["post", "user"]


class PostFavorOwnedListSchemaOut(ModelSchema):
    """
    用于用户查询自己点赞的post返回的schema，不用包含用户信息
    """
    post: PostSchemaListOut

    class Config:
        model = PostFavor
        include = ["post", "create_time"]


class PostCommentCreateUpdateSchemaOne(ModelSchema):
    """
    用于创建修改帖子评论序列化展示
    """

    class Config:
        model = PostComment
        include = ["content"]

    # 创建帖子评论
    def create_post_comment(self, **kwargs: Any) -> Type[PostComment]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return PostComment.objects.create(**_data)

    # 更新帖子评论
    def update_post_comment(self, instance: Any, **kwargs: Any) -> Any:
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PostCommentSchemaOut(ModelSchema):
    """
    用于返回帖子评论序列化展示
    """
    user: UserNameSchema

    class Config:
        model = PostComment
        include = "__all__"
