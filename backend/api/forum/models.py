import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
UserModel = get_user_model()


class PostTag(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False,
                            verbose_name='标签名称', help_text='标签名称')
    description = models.TextField(default="", null=True, blank=True,
                                   verbose_name="标签描述", help_text="标签描述")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间', help_text='修改时间')

    class Meta:
        verbose_name = '帖子标签'
        verbose_name_plural = verbose_name
        db_table = 'post_tag'

    def __str__(self):
        return self.name


class PostInfo(models.Model):
    # 文章ID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name="评论ID", help_text="评论ID")
    # 文章列表页内容
    title = models.CharField(max_length=100, null=False, blank=False,
                             verbose_name="帖子标题", help_text="帖子标题")
    tag = models.ForeignKey(PostTag, null=True, blank=True, on_delete=models.SET_NULL,
                            verbose_name='文章标签', related_name='tag_posts')
    front_image = models.ImageField(upload_to="image/post/front_image", null=True, blank=True,
                                    verbose_name="封面图", help_text="封面图")
    brief_content = models.CharField(max_length=200, default="", blank=True,
                                     verbose_name="帖子简介", help_text="帖子简介")
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False, blank=False,
                               verbose_name="发帖人", help_text="发帖人")

    # 文章内容，之后用富文本编辑器来实现
    content = models.TextField(max_length=100000, null=False, blank=False,
                               verbose_name="帖子正文", help_text="帖子正文")

    click_num = models.PositiveIntegerField(default=0, verbose_name='浏览量', help_text='浏览量')
    comment_num = models.PositiveIntegerField(default=0, verbose_name='评论数', help_text='评论数')
    favor_num = models.PositiveIntegerField(default=0, verbose_name='点赞数', help_text='点赞数')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间', help_text='修改时间')

    class Meta:
        verbose_name = '帖子信息'
        verbose_name_plural = verbose_name
        db_table = 'post_info'
        ordering = ["-create_time"]

    def __str__(self):
        return self.title


class PostFavor(models.Model):
    """
    用户点赞表
    """
    post = models.ForeignKey(PostInfo, on_delete=models.CASCADE, verbose_name="商品", help_text="商品", )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="post_favor",
                             verbose_name="用户", help_text="用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_favor_post_user')
        ]
        verbose_name = '帖子点赞信息'
        verbose_name_plural = verbose_name
        db_table = 'post_favor_info'


class PostComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name="评论ID", help_text="评论ID")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user_post_comment",
                             verbose_name="评论者", help_text="评论者")
    post = models.ForeignKey(PostInfo, on_delete=models.CASCADE, related_name="post_comment",
                             verbose_name="帖子", help_text="帖子")
    # 评论内容，之后用富文本编辑器来实现
    content = models.TextField(max_length=100000, null=False, blank=False,
                               verbose_name="评论内容", help_text="评论内容")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="修改时间", help_text="修改时间")

    class Meta:
        verbose_name = '帖子评论'
        verbose_name_plural = verbose_name
        db_table = 'post_comment'
        ordering = ["-create_time"]
