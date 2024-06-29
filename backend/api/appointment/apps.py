from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.appointment'
    verbose_name = '挂号预约管理'