# 作   者：林枭熠
# 开发时间:2024/6/10 下午8:30
from django.db import transaction
from ninja import Query
from ninja_extra import api_controller, ControllerBase, route, status
from ninja_extra.ordering import ordering, Ordering
from ninja_extra.pagination import (
    paginate, PageNumberPaginationExtra, PaginatedResponseSchema
)
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from api.shop.goods.Filter import GoodsFilterSchema, GoodsFavorFilterSchema, GoodsCategoryFilterSchema
from api.shop.goods.models import GoodsInfo, GoodsCategory, GoodsFavor
from api.shop.goods.schema import GoodsSchemaOut, CategorySchema1, CategorySchema2, \
    GoodFavorDetailedSchemaOut, GoodFavorOwnedListSchemaOut


@api_controller("/shop/goods", tags=["goods"])
class GoodsController(ControllerBase):
    """
    用于商品管理的API控制器，只用来查询，无权限认证
    """
    @route.get(
        '',
        response=PaginatedResponseSchema[GoodsSchemaOut],
        url_name="get-goods-list",
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['create_time', 'sold_num', "price"])
    def list_goods(self, filters: Query[GoodsFilterSchema]):
        """
        获取商品列表，并进行排序和分页，无权限认证，搜索字段：['search', 'category', 'parent_category', 'is_hot', "is_new"]

        search：商品name、content模糊搜索

        category：商品二级类目name模糊搜索

        parent_category：商品一级类目name模糊搜索

        is_hot：是否热门商品，Q(sold_num__gt=10) | Q(is_hot=True)

        is_new：是否新品，创建时间在7天以内的为新品  Q(create_time__gt=seven_days_ago) | Q(is_new=True)
        """
        Goods = GoodsInfo.objects.all()
        Goods = filters.filter(Goods)
        return Goods

    @route.get(
        "/{uuid:good_id}",
        response=GoodsSchemaOut,
        url_name="get-one-good-detail"
    )
    def retrieve_good(self, good_id: str):
        """
        输入商品id，获取商品详情，并更新点击数，无权限认证
        """
        good = self.get_object_or_exception(
            GoodsInfo.objects.all(),
            id=good_id,
            error_message=f"id为 {good_id} 的商品不存在",
        )
        # 商品点击数+1
        good.click_num += 1
        good.save()
        return good

    @route.put(
        "/favor/{uuid:good_id}",
        response={201: GoodFavorDetailedSchemaOut, 204: None},
        url_name="add-good-to-favor",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def favor_good(self, good_id: str):
        """
        添加商品到点赞列表，或者取消点赞，有权限认证，需要登录
        """
        user = self.context.request.user
        good = self.get_object_or_exception(
            GoodsInfo.objects.all(),
            id=good_id,
            error_message=f"id为 {good_id} 的商品不存在",
        )
        exists = GoodsFavor.objects.filter(good=good, user=user).exists()
        # 未点赞，创建点赞记录，点赞数+1
        if not exists:
            good.favor_num += 1
            good.save()
            return 201, GoodsFavor.objects.create(good=good, user=user)
        # 已点赞，删除点赞记录，点赞数-1
        else:
            good.favor_num -= 1
            good.save()
            favor = GoodsFavor.objects.get(good=good, user=user)
            favor.delete()
            return self.create_response("点赞已取消", status_code=status.HTTP_204_NO_CONTENT)

    @route.get(
        '/favor',
        response=PaginatedResponseSchema[GoodFavorOwnedListSchemaOut],
        url_name="get-user's-good-favor-list",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['create_time'])
    def list_good_favors(self, filters: Query[GoodsFavorFilterSchema]):
        """
        获取用户的点赞列表，有权限认证，需要登录，只能访问自己的点赞列表，搜索字段：['good_name', 'good_category', 'good_parent_category', 'is_hot', "is_new"]

        good_name：商品name模糊搜索

        good_category：商品二级类目name模糊搜索

        good_parent_category：商品一级类目name模糊搜索

        is_hot：是否热门商品

        is_new：是否新品


        """
        favor_queryset = GoodsFavor.objects.filter(user=self.context.request.user)
        favor_queryset = filters.filter(favor_queryset)
        return favor_queryset


@api_controller("/shop/goods/category", tags=["good_category"])
class GoodCategoryController(ControllerBase):
    """
    用于商品类目管理的API控制器，只用来查询，无权限认证
    """

    @route.get(
        '',
        response=PaginatedResponseSchema[CategorySchema1],
        url_name="get-goods_category-list",
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['create_time'])
    def list_good_category(self, filters: Query[GoodsCategoryFilterSchema]):
        """
        获取商品一级类目列表，包含嵌套的二级类目列表，无权限认证，搜索字段：['name'，'description']

        name: 类目名称模糊搜索

        description: 类目描述模糊搜索
        """
        queryset = GoodsCategory.objects.filter(category_type=1)
        queryset = filters.filter(queryset)
        return queryset

    @route.get(
        "/Level1/{uuid:good_category_id}",
        response=CategorySchema1,
        url_name="get-one-Level1_good_category_detail"
    )
    def retrieve_good_category_1(self, good_category_id: str):
        """
        获取一级标题类目详情，无权限认证
        """
        good_category = self.get_object_or_exception(
            GoodsCategory.objects.filter(category_type=1),
            id=good_category_id,
            error_message=f"id为 {good_category_id} 的一级标题类目不存在",
        )
        return good_category

    @route.get(
        "/Level2/{uuid:good_category_id}",
        response=CategorySchema2,
        url_name="get-one-Level2-good_category_detail"
    )
    def retrieve_good_category_2(self, good_category_id: str):
        """
        获取二级标题类目详情，无权限认证
        """
        good_category = self.get_object_or_exception(
            GoodsCategory.objects.filter(category_type=2),
            id=good_category_id,
            error_message=f"id为 {good_category_id} 的二级标题类目不存在",
        )
        return good_category
