# 作   者：林枭熠
# 开发时间:2024/6/16 下午4:27
from datetime import timedelta, datetime
from typing import Optional

from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import make_aware
from ninja import FilterSchema
from pydantic import Field


class PostFilterSchema(FilterSchema):
    """
    帖子过滤Schema，用于帖子列表的过滤搜索
    """
    # 帖子标题名称、简介搜索：search
    search: Optional[str] = Field(None, q=['title__icontains',
                                           'brief_content__icontains'])
    # 帖子作者名称搜索：author
    author: Optional[str] = Field(None, q=['author__username__icontains'])
    # 帖子标签搜索：tag
    tag: Optional[str] = Field(None, q=['tag__name__icontains'])
    # 商品是否热销：is_hot
    is_hot: Optional[bool] = None
    # 商品是否新品：is_new
    is_new: Optional[bool] = None

    def filter_is_hot(self, value: bool) -> Q:
        return Q(click_num__gt=10) | Q(favor_num__gt=5) | Q(comment_num__gt=3) if value else Q()

    def filter_is_new(self, value: bool) -> Q:
        three_days_ago = make_aware(timezone.now() - timedelta(days=3))
        return Q(create_time__gt=three_days_ago) if value else Q()


class PostCommentFilterSchema(FilterSchema):
    """
    帖子评论过滤Schema，用于帖子评论列表的过滤搜索
    """
    # 帖子id post_id: post_id
    post_id: Optional[str] = Field(None, q=["post__id__icontains"])
    # 用户id user_id：user_id
    user_id: Optional[str] = Field(None, q=['user__id__icontains'])
    # 用户名user_username：user_username
    user_username: Optional[str] = Field(None, q=['user__username__icontains'])
