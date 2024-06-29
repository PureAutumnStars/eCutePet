import uuid

from django.contrib.auth import get_user_model
from django.db import models

from api.shop.goods.models import GoodsInfo

# Create your models here.

UserModel = get_user_model()


class OrderInfo(models.Model):
    """
    订单模型
    """
    id = models.CharField(primary_key=True, max_length=30, null=False, blank=False, unique=True,
                          verbose_name="订单号", help_text="订单号")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_order',
                             verbose_name="用户", help_text="用户")
    good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, related_name='good_order',
                             verbose_name="商品名称", help_text="商品名称")
    order_amount = models.FloatField(default=0.0, verbose_name="订单金额", help_text="订单金额")

    # 用户信息
    is_sign = models.BooleanField(default=False, verbose_name="是否签收", help_text="是否签收")
    address = models.CharField(max_length=100, verbose_name="收货地址", help_text="收货地址")
    signer_name = models.CharField(max_length=20, default="匿名", verbose_name="签收人", help_text="签收人姓名")
    signer_mobile = models.CharField(max_length=11, verbose_name="联系电话", help_text="联系电话")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")
    sign_time = models.DateTimeField(null=True, blank=True, verbose_name="签收时间", help_text="签收时间")

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name
        db_table = 'order_info'

    def __str__(self):
        return self.id


class GoodsComment(models.Model):
    """
    商品评论
    """
    RATING_TYPE = (
        (1, "一星"),
        (2, "两星"),
        (3, "三星"),
        (4, "四星"),
        (5, "五星"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name="评论ID", help_text="评论ID")
    order = models.OneToOneField(OrderInfo, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name="order_comment",
                                 verbose_name="订单", help_text="订单")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user_good_comment",
                             verbose_name="用户", help_text="用户")
    good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, related_name="good_comment",
                             verbose_name="商品", help_text="商品")

    rating = models.IntegerField(choices=RATING_TYPE, verbose_name="评分", help_text="评分")
    content = models.CharField(default="", max_length=300, verbose_name="评论内容", help_text="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="修改时间", help_text="修改时间")

    class Meta:
        verbose_name = '商品评论'
        verbose_name_plural = verbose_name
        db_table = 'goods_comment'

    def __str__(self):
        return self.id
