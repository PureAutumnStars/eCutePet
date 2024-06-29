import uuid

from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


# Create your models here.
class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name="商品类别ID", help_text="商品类别ID")
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    # code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    description = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True,
                                        verbose_name="父类目级别", help_text="父类别目录",
                                        related_name="sub_category", on_delete=models.SET_NULL)
    # is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name
        db_table = "goods_category"

    def __str__(self):
        return self.name


class GoodsInfo(models.Model):
    """
    商品信息
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name="商品ID", help_text="商品ID")
    category = models.ForeignKey(GoodsCategory, null=True, blank=True,
                                 verbose_name="商品类目", help_text="商品类目",
                                 on_delete=models.SET_NULL, related_name="sub_goods")
    name = models.CharField(max_length=100, verbose_name="商品名", help_text="商品名")
    content = models.TextField(default="", verbose_name="商品详情", help_text="商品详情")
    front_image = models.ImageField(upload_to="image/shop", null=True, blank=True,
                                    verbose_name="封面图", help_text="封面图")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="售价", help_text="售价")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="修改时间", help_text="修改时间")

    sold_num = models.PositiveIntegerField(default=0, verbose_name="销量", help_text="销量")
    click_num = models.PositiveIntegerField(default=0, verbose_name="点击数", help_text="点击数")
    comment_num = models.PositiveIntegerField(default=0, verbose_name="评论数", help_text="评论数")
    favor_num = models.PositiveIntegerField(default=0, verbose_name="赞数", help_text="赞数")

    is_new = models.BooleanField(default=False, verbose_name="是否新品", help_text="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销", help_text="是否热销")
    is_ship_free = models.BooleanField(default=True, verbose_name="是否承担运费", help_text="是否承担运费")

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name
        db_table = 'goods_info'

    def __str__(self):
        return self.name


class GoodsFavor(models.Model):
    """
    用户点赞表
    """
    good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="商品", help_text="商品",)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="good_favor",
                             verbose_name="用户", help_text="用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['good', 'user'], name='unique_favor_good_user')
        ]
        verbose_name = '商品点赞信息'
        verbose_name_plural = verbose_name
        db_table = 'good_favor_info'

    def __str__(self):
        return self.good.name
