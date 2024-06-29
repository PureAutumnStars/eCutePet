# 作   者：林枭熠
# 开发时间:2024/6/10 下午8:30
from datetime import datetime

from django.db import transaction
from ninja import Query
from ninja_extra import api_controller, ControllerBase, route, status
from ninja_extra.ordering import ordering, Ordering
from ninja_extra.pagination import (
    paginate, PageNumberPaginationExtra, PaginatedResponseSchema
)
from ninja_extra.permissions import IsAuthenticated, IsAdminUser
from ninja_jwt.authentication import JWTAuth

from api.shop.goods.models import GoodsInfo
from api.shop.trades.Filter import GoodsOrderFilterSchema, GoodsCommentFilterSchema
from api.shop.trades.models import OrderInfo, GoodsComment
from api.shop.trades.schema import OrderCreateSchemaIn, OrderSchemaOut, OrderUpdateSchemaIn, \
    GoodCommentCreateUpdateSchemaIn, GoodCommentDetailedSchemaOut, GoodCommentListSchemaOut, ErrorMessage
from utils.permissions import IsOwnerOrReadOnly


@api_controller("/shop/trades/order", tags=["orders"], auth=JWTAuth())
class OrderController(ControllerBase):
    """
    订单相关接口
    """

    # 新建订单
    @route.post(
        "create/{uuid:good_id}",
        response={201: OrderSchemaOut},
        url_name="create-order",
        permissions=[IsAuthenticated | IsAdminUser]
    )
    def create_order(self, order_schema: OrderCreateSchemaIn, good_id: str):
        """
        新建订单，额外传入参数为商品id，需要用户自身权限
        """
        good_instance = self.get_object_or_exception(
            GoodsInfo.objects.all(),
            id=good_id,
            error_message=f"id为 {good_id} 的商品不存在",
        )
        order_amount = good_instance.price
        order_instance = order_schema.create_order(user=self.context.request.user, good=good_instance,
                                                   order_amount=order_amount)
        return 201, order_instance

    @route.get(
        "",
        response=PaginatedResponseSchema[OrderSchemaOut],
        url_name="get-user-owned-order-list",
        permissions=[IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['create_time', 'sign_time', "order_amount"])
    def list_orders(self, filters: Query[GoodsOrderFilterSchema]):
        """
        获取访问用户的所有订单列表，需要用户自身权限， 过滤参数：['good_name', 'good_brief_content', 'good_category_name']

        good_name：订单中商品name模糊搜索

        good_brief_content：商品简介brief_content模糊搜索

        good_category：商品二级类目name模糊搜索
        """
        queryset = OrderInfo.objects.filter(user=self.context.request.user)
        queryset = filters.filter(queryset)
        return queryset

    @route.get(
        "/{str:order_id}",
        response={200: OrderSchemaOut},
        url_name="get-one-order-detail",
        permissions=[IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
    )
    def retrieve_order(self, order_id: str):
        """
        获取用户相关的某一订单详情，需要用户自身权限
        """
        order_instance = self.get_object_or_exception(
            OrderInfo.objects.filter(user=self.context.request.user),
            id=order_id,
            error_message=f"id为 {order_id} 的商品订单不存在，或不是当前用户的订单",
        )
        return 200, order_instance

    @route.put(
        "/{str:order_id}",
        response={200: OrderSchemaOut, 400: ErrorMessage},
        url_name="update-order",
        permissions=[IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
    )
    @transaction.atomic
    def update_order(self, order_id: str, order_schema: OrderUpdateSchemaIn):
        """
        更新订单，具体字段为：["is_sign", "address", "signer_name", "signer_mobile"]，且需要用户自身权限

        当is_sign第一次被设置为true后相当于签收了，之后就不能更改订单信息了
        """
        order_instance = self.get_object_or_exception(
            OrderInfo.objects.filter(user=self.context.request.user),
            id=order_id,
            error_message=f"id为 {order_id} 的商品订单不存在，或不是当前用户的订单",
        )
        if order_schema.is_sign:
            if order_instance.is_sign:
                return 400, dict(message="订单已签收，无法更改订单信息")
            order_instance.sign_time = datetime.now()
            order_instance.good.sold_num += 1
            order_instance.good.save()
        order = order_schema.update(order_instance)
        return 200, order

    @route.delete(
        "/{str:order_id}",
        url_name="delete-order",
        response={204: dict},
        permissions=[IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
    )
    @transaction.atomic
    def delete_order(self, order_id: str):
        """
        删除订单，需要用户自身权限
        """
        order = self.get_object_or_exception(
            OrderInfo.objects.filter(user=self.context.request.user),
            id=order_id,
            error_message=f"id为 {order_id} 的商品订单不存在，或不是当前用户的订单",
        )
        order.delete()
        return self.create_response("订单成功删除", status_code=status.HTTP_204_NO_CONTENT)


@api_controller("/shop/trades/comment", tags=["good_comments"], auth=JWTAuth())
class GoodCommentController(ControllerBase):
    """
    商品评论相关接口
    """

    @route.post(
        "create/{str:order_id}",
        response={201: GoodCommentDetailedSchemaOut, 400: ErrorMessage},
        url_name="create-good-comment",
        permissions=[IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
    )
    @transaction.atomic
    def create_good_comment(self, comment_schema: GoodCommentCreateUpdateSchemaIn, order_id: str):
        """
        新建订单商品评论，只能创建用户购买的，且已经签收的订单对应的评论，且需要用户自身权限，订单未签收时不能评论
        """
        order_instance = self.get_object_or_exception(
            OrderInfo.objects.filter(user=self.context.request.user),
            id=order_id,
            error_message=f"id为 {order_id} 的商品订单不存在，或不是当前用户的订单",
        )
        if not order_instance.is_sign:
            return 400, dict(message="订单还未签收，无法评论")
        user = self.context.request.user
        good = order_instance.good
        good.comment_num += 1
        good.save()
        comment_instance = comment_schema.create_comment(order=order_instance, user=user, good=good)
        return 201, comment_instance

    @route.get(
        "",
        response=PaginatedResponseSchema[GoodCommentListSchemaOut],
        url_name="get-good-comment-list",
        auth=None,
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['create_time', 'modify_time', "rating"])
    def list_good_comments(self, filters: Query[GoodsCommentFilterSchema]):
        """
        获取所有商品评论列表，返回的评论信息不包含敏感订单信息和用户信息，不需要用户权限，不登录也能查看商品评论

        搜索参数列表：["good_id", "good_name", "good_category", "rating", "user_id", "user_username"]

        good_id：商品id搜索

        good_name：商品name模糊搜索

        good_category：商品二级类目name模糊搜索

        rating：评论星级搜索

        user_id：用户id搜索

        user_username：用户username模糊搜索
        """
        queryset = GoodsComment.objects.all()
        queryset = filters.filter(queryset)
        return queryset

    @route.get(
        "{uuid:comment_id}",
        response={200: GoodCommentDetailedSchemaOut},
        url_name="get-one-good-comment",
        permissions=[IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
    )
    def retrieve_good_comment(self, comment_id: str):
        """
        获取单一商品评论信息，返回的评论信息包含敏感订单信息和用户信息，需要用户自身权限
        """
        good_comment_instance = self.get_object_or_exception(
            GoodsComment.objects.filter(user=self.context.request.user),
            id=comment_id,
            error_message=f"id为 {comment_id} 的商品评论详情不存在，或不是当前用户的评论",
        )
        return 200, good_comment_instance

    @route.put(
        "/update/{uuid:comment_id}",
        response={200: GoodCommentDetailedSchemaOut},
        url_name="update-good-comment",
        permissions=[IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
    )
    @transaction.atomic
    def update_good_comment(self, comment_id: str, comment_schema: GoodCommentCreateUpdateSchemaIn):
        """
        更新商品评论，只能更新用户购买的，且已经签收的订单对应的评论，具体字段为：rating、content，且需要用户自身权限
        """
        comment_instance = self.get_object_or_exception(
            GoodsComment.objects.filter(user=self.context.request.user),
            id=comment_id,
            error_message=f"id为 {comment_id} 的商品评论详情不存在，或不是当前用户的评论",
        )
        comment = comment_schema.update_comment(comment_instance)
        return 200, comment

    @route.delete(
        "/delete/{uuid:comment_id}",
        url_name="delete-good-comment",
        response={204: dict},
        permissions=[IsAuthenticated, IsOwnerOrReadOnly | IsAdminUser]
    )
    @transaction.atomic
    def delete_comment(self, comment_id: str):
        """
        删除订单，需要用户自身权限
        """
        comment_instance = self.get_object_or_exception(
            GoodsComment.objects.filter(user=self.context.request.user),
            id=comment_id,
            error_message=f"id为 {comment_id} 的商品评论详情不存在，或不是当前用户的评论",
        )
        comment_instance.good.comment_num -= 1
        comment_instance.good.save()
        comment_instance.delete()
        return self.create_response("评论成功删除", status_code=status.HTTP_204_NO_CONTENT)
