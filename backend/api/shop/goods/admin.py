from django.contrib import admin

from api.shop.goods.models import GoodsCategory, GoodsInfo, GoodsFavor


# Register your models here.

@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    # 默认按照category_type排序
    ordering = ['category_type']

    # 自定义后台展示的信息
    list_display = ["category_type", "name", "description", "parent_category", "create_time"]


@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    # 默认按照price排序
    ordering = ['price']

    # 自定义后台展示的信息
    list_display = ["name", "category", "price", "sold_num", "click_num", "favor_num", "create_time"]


@admin.register(GoodsFavor)
class GoodsFavorAdmin(admin.ModelAdmin):
    # 默认按照create_time排序
    ordering = ['create_time']

    # 自定义后台展示的信息
    list_display = ["user", "good", "create_time"]
