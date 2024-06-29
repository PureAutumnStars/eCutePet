# 作   者：林枭熠
# 开发时间:2024/6/18 下午6:36

# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Appointment


@shared_task
def update_status():
    now = timezone.now()
    one_day_later = now + timezone.timedelta(days=1)

    # 更新Pending状态为Confirmed
    appointments = Appointment.objects.filter(status='Pending', appointment_time__lte=one_day_later)
    for appointment in appointments:
        appointment.status = 'Confirmed'
        appointment.save()

    # 更新Confirmed状态为Completed
    appointments = Appointment.objects.filter(status='Confirmed', appointment_time__lte=now)
    for appointment in appointments:
        appointment.status = 'Completed'
        appointment.save()

        # 更新DoctorInfo的reception_num属性
        doctor = appointment.doctor
        doctor.reception_num += 1
        doctor.save()
