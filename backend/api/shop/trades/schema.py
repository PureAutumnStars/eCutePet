# 作   者：林枭熠
# 开发时间:2024/6/13 下午7:23
import time
from typing import Type, Any, Optional

from django.db import transaction
from ninja_schema import ModelSchema, Schema
from pydantic import Field

from api.shop.goods.schema import GoodsSchemaOut
from api.shop.trades.models import OrderInfo, GoodsComment
from api.users.schema import UserRetrieveOutSchema, UserNameSchema


class ErrorMessage(Schema):
    message: str


class OrderCreateSchemaIn(ModelSchema):
    class Config:
        model = OrderInfo
        include = ["address", "signer_name", "signer_mobile"]
        optional = ["signer_name"]

    # 创建订单
    @transaction.atomic
    def create_order(self, **kwargs) -> Type[OrderInfo]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        _data["id"] = self.generate_order_id(user_id=_data.get("user"))
        return OrderInfo.objects.create(**_data)

    @staticmethod
    def generate_order_id(user_id):
        # 当前时间(精确到秒数)+user_id+随机数
        from random import Random
        random_ins = Random()
        order_id = "{time_str}{user_id}{random_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                            user_id=user_id,
                                                            random_str=random_ins.randint(10, 99))

        return order_id


class OrderUpdateSchemaIn(ModelSchema):
    class Config:
        model = OrderInfo
        include = ["is_sign", "address", "signer_name", "signer_mobile"]
        optional = ["is_sign", "address", "signer_name", "signer_mobile"]

    # 更新订单
    def update(self, instance: Any, **kwargs: Any) -> Any:
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class OrderSchemaOut(ModelSchema):
    user: UserRetrieveOutSchema
    good: GoodsSchemaOut

    class Config:
        model = OrderInfo
        include = "__all__"


class GoodCommentCreateUpdateSchemaIn(ModelSchema):
    rating: int = Field(..., ge=1, le=5)

    class Config:
        model = GoodsComment
        include = ["rating", "content"]
        optional = ["content"]

    # 创建评论
    def create_comment(self, **kwargs) -> Type[GoodsComment]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return GoodsComment.objects.create(**_data)

    # 更新评论
    def update_comment(self, instance: Any, **kwargs: Any) -> Any:
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GoodCommentDetailedSchemaOut(ModelSchema):
    """
    订单详情中商品评论的详细信息，包含订单信息和个人信息这些敏感的信息
    """
    order: Optional[OrderSchemaOut] = None

    class Config:
        model = GoodsComment
        include = ["id", "order", "rating", "content", "create_time", "modify_time"]


class GoodCommentListSchemaOut(ModelSchema):
    good: GoodsSchemaOut
    user: UserNameSchema

    class Config:
        model = GoodsComment
        include = ["id", "good", "user", "rating", "content", "create_time", "modify_time"]
