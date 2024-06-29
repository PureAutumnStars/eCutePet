# 作   者：林枭熠
# 开发时间:2024/6/14 下午8:03
from datetime import timedelta
from typing import Optional

from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import make_aware
from ninja import FilterSchema, Field


class GoodsFilterSchema(FilterSchema):
    """
    商品过滤Schema，用于商品列表的过滤搜索
    """
    # 商品名称、内容搜索：search
    search: Optional[str] = Field(None, q=['name__icontains',
                                           'content__icontains'])
    # 商品二级类别搜索：category
    category: Optional[str] = Field(None, q=['category__name__icontains'])
    # 商品一级类别搜索：parent_category
    parent_category: Optional[str] = Field(None, q=['category__parent_category__name__icontains'])
    # 商品是否热销：is_hot
    is_hot: Optional[bool] = None
    # 商品是否新品：is_new
    is_new: Optional[bool] = None

    def filter_is_hot(self, value: bool) -> Q:
        return Q(sold_num__gt=10) | Q(is_hot=True) if value else Q()

    def filter_is_new(self, value: bool) -> Q:
        seven_days_ago = make_aware(timezone.now() - timedelta(days=7))
        return Q(create_time__gt=seven_days_ago) | Q(is_new=True) if value else Q()


class GoodsFavorFilterSchema(FilterSchema):
    """
    用户点赞商品过滤Schema，用于用户点赞商品列表的过滤搜索
    """
    # 商品名称name：good_name
    good_name: Optional[str] = Field(None, q=['good__name__icontains'])
    # 商品二级类别搜索：good_category
    good_category: Optional[str] = Field(None, q=['good__category__name__icontains'])
    # 商品一级类别搜索：good_parent_category
    good_parent_category: Optional[str] = Field(None, q=['good__category__parent_category__name__icontains'])
    # 商品是否热销：is_hot
    is_hot: Optional[bool] = None
    # 商品是否热销：is_new
    is_new: Optional[bool] = None

    def filter_is_hot(self, value: bool) -> Q:
        return Q(sold_num__gt=10) | Q(is_hot=True) if value else Q()

    def filter_is_new(self, value: bool) -> Q:
        seven_days_ago = make_aware(timezone.now() - timedelta(days=7))
        return Q(create_time__gt=seven_days_ago) | Q(is_new=True) if value else Q()


class GoodsCategoryFilterSchema(FilterSchema):
    """
    商品类目过滤Schema，用于商品类目的过滤搜索
    """
    # 商品类目名称name：name
    name: Optional[str] = Field(None, q=['name__icontains'])
    # 商品类目描述description：category
    description: Optional[str] = Field(None, q=['description__icontains'])
