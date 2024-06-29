from django.contrib import admin

from api.shop.trades.models import OrderInfo, GoodsComment


# Register your models here.

@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    # 默认按照id排序
    ordering = ['id']

    # 自定义后台展示的信息
    list_display = ["id", "user", "good", "order_amount", "is_sign", "create_time", "sign_time"]


@admin.register(GoodsComment)
class GoodsCommentAdmin(admin.ModelAdmin):
    # 默认按照id排序
    ordering = ['id']

    # 自定义后台展示的信息
    list_display = ["id", "good", "user", "rating", "create_time", "modify_time"]
