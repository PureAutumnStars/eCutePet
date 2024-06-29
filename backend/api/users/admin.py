from django.contrib import admin

from api.users.models import UserInfo, DoctorInfo, VerifyCode

# Register your models here.

admin.site.site_header = 'E-萌宠后台管理系统'
admin.site.site_title = 'E-萌宠后台管理系统'
admin.site.index_title = '首页'


@admin.register(VerifyCode)
class VerifyCodeAdmin(admin.ModelAdmin):
    # 默认按照add_time排序
    ordering = ['add_time']

    # 自定义后台展示的信息
    list_display = ["code_type", "email", "code", "add_time"]


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    # 默认按照id排序
    ordering = ['id']

    # 自定义后台展示的信息
    list_display = ["id", "username", "email", "is_doctor", "is_active", "is_staff", "date_joined"]


@admin.register(DoctorInfo)
class DoctorInfoAdmin(admin.ModelAdmin):
    # 默认按照id排序
    ordering = ['id']

    # 自定义后台展示的信息
    list_display = ["id", "ID_number", "real_name", "certificate_number",
                    "is_service", "reception_num", "post_num"]
