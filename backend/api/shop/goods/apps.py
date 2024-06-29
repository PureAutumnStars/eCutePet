from django.apps import AppConfig


class GoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.shop.goods'
    verbose_name = '商品管理'
