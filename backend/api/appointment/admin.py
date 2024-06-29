from django.contrib import admin

from api.appointment.models import DoctorWeeklyAvailability, PatientInfo, Appointment


# Register your models here.

@admin.register(DoctorWeeklyAvailability)
class DoctorAvailableTimeAdmin(admin.ModelAdmin):
    # 默认按照医生名，星期几，和开始日期排序
    ordering = ['doctor', 'day_of_week', 'start_time']

    # 自定义后台展示的信息
    list_display = ["doctor", "day_of_week", "start_time", "end_time"]


@admin.register(PatientInfo)
class PatientInfoAdmin(admin.ModelAdmin):
    # 默认按照用户名排序
    ordering = ['user']

    # 自定义后台展示的信息
    list_display = ["user", "real_name", "phone_number", "ID_number"]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # 默认按照预约时间、预约医生、预约病人排序
    ordering = ['appointment_time', 'doctor', 'patient']

    # 自定义后台展示的信息
    list_display = ["id", "appointment_time", "doctor", "patient", "status"]
