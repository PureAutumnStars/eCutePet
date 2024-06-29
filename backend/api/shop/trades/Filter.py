# 作   者：林枭熠
# 开发时间:2024/6/15 下午2:47
from typing import Optional

from ninja import FilterSchema
from pydantic import Field


class GoodsOrderFilterSchema(FilterSchema):
    """
    商品订单过滤Schema，用于商品订单的过滤搜索
    """
    # 商品名称good_name：good_name
    good_name: Optional[str] = Field(None, q=['good__name__icontains'])

    # 商品类目名称good_category_name：good_category_name
    good_category_name: Optional[str] = Field(None, q=['good__category__name__icontains'])


class GoodsCommentFilterSchema(FilterSchema):
    """
    商品订单评论过滤Schema，用于商品订单评论的过滤搜索
    """
    # 商品名称good_id：good_id
    good_id: Optional[str] = Field(None, q=['good__id__icontains'])
    # 商品名称good_name：good_name
    good_name: Optional[str] = Field(None, q=['good__name__icontains'])
    # 商品类目good_category：good_category
    good_category: Optional[str] = Field(None, q=['good__category__name__icontains'])
    # 商品评分rating：rating
    rating: Optional[int] = Field(None, q=['rating__icontains'])
    # 用户id user_id：user_id
    user_id: Optional[str] = Field(None, q=['user__id__icontains'])
    # 用户名user_username：user_username
    user_username: Optional[str] = Field(None, q=['user__username__icontains'])
