# 作   者：林枭熠
# 开发时间:2024/6/13 上午11:55
from typing import List, Annotated


from ninja_extra import service_resolver
from ninja_extra.controllers import RouteContext
from ninja_schema import ModelSchema, model_validator
from pydantic import AnyUrl, field_validator

from api.shop.goods.models import GoodsCategory, GoodsInfo, GoodsFavor
from api.users.schema import UserRetrieveOutSchema


class CategorySchema2(ModelSchema):
    """
    商品二级类别序列化
    """

    class Config:
        model = GoodsCategory
        include = ["id", "name", "description", "category_type", "parent_category"]
        optional_fields = ["description"]
        depth = 1


class CategorySchema1(ModelSchema):
    """
    商品一级类别序列化
    """
    sub_category: List[CategorySchema2] = []

    def resolve_sub_category(self, obj):
        queryset = GoodsCategory.objects.filter(parent_category=self.id, category_type=2)
        return queryset

    class Config:
        model = GoodsCategory
        include = ["id", "name", "description", "category_type"]
        optional_fields = ["description"]
        depth = 1


# class GoodsCreateSchemaIn(ModelSchema):
#     """
#     用于返回创建商品的输入Schema
#     """
#     category: CategorySchema2 = None
#
#     class Config:
#         model = GoodsInfo
#         include = ["name", "category", "brief_content", "content", "front_image",
#                    "price", "is_new", "is_hot", "is_ship_free"]
#         optional = ["brief_content", "content", "front_image",
#                     "is_new", "is_hot", "is_ship_free"]
#         depth = 1
#
#     def create(self, **kwargs) -> Type[GoodsInfo]:
#         data = self.dict()
#         data.update(kwargs)
#         return GoodsInfo.objects.create(**data)
class GoodsCategorySchema(ModelSchema):
    """
    用于返回商品类别信息name的Schema
    """

    class Config:
        model = GoodsCategory
        include = ["name", "description", "category_type"]


class GoodsSchemaOut(ModelSchema):
    """
    用于返回商品信息的Schema
    """
    category: GoodsCategorySchema

    @field_validator("front_image")
    def front_image_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        return context.request.build_absolute_uri(value_data)

    class Config:
        model = GoodsInfo
        include = "__all__"


class GoodFavorDetailedSchemaOut(ModelSchema):
    """
    用于点赞详情返回的schema，包含商品信息和用户信息
    """
    good: GoodsSchemaOut
    user: UserRetrieveOutSchema

    class Config:
        model = GoodsFavor
        include = ["good", "user"]


class GoodFavorOwnedListSchemaOut(ModelSchema):
    """
    用于用户查询自己点赞返回的schema，不用包含用户信息
    """
    good: GoodsSchemaOut

    class Config:
        model = GoodsFavor
        include = ["good", "create_time"]
