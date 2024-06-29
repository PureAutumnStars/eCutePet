import uuid

from django.contrib.auth import get_user_model
from django.db import models

from api.users.models import DoctorInfo

# Create your models here.

UserModel = get_user_model()


class PatientInfo(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='patient',
                                verbose_name='用户', help_text='用户')
    real_name = models.CharField(max_length=32, verbose_name="真实姓名", help_text="真实姓名")
    ID_number = models.CharField(max_length=32, verbose_name="身份证号", help_text="身份证号")
    phone_number = models.CharField(max_length=32, verbose_name="手机号", help_text="手机号")

    class Meta:
        verbose_name = '患者信息'
        verbose_name_plural = verbose_name
        db_table = 'patient_info'

    def __str__(self):
        return self.real_name + "_" + self.phone_number


class DoctorWeeklyAvailability(models.Model):
    WEEK_TYPE = (
        (1, '星期一'),
        (2, '星期二'),
        (3, '星期三'),
        (4, '星期四'),
        (5, '星期五'),
        (6, '星期六'),
        (7, '星期天')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name="医生接诊时间ID", help_text="医生接诊时间ID")
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, null=False, blank=False,
                               related_name='weekly_available_time',
                               verbose_name='医生', help_text='医生')
    day_of_week = models.IntegerField(choices=WEEK_TYPE, null=False, blank=False,
                                      verbose_name='星期几', help_text='星期几')
    start_time = models.TimeField(null=False, blank=False, verbose_name='开始时间', help_text='开始时间')
    end_time = models.TimeField(null=False, blank=False, verbose_name='结束时间', help_text='结束时间')

    class Meta:
        verbose_name = '医生可预约时间信息'
        verbose_name_plural = verbose_name
        db_table = 'doctor_available_time'
        ordering = ["doctor", "day_of_week", "start_time", "end_time"]

    def __str__(self):
        return f"{self.doctor} available on {self.day_of_week} from {self.start_time} to {self.end_time}"


class Appointment(models.Model):
    APPOINTMENT_STATUS = (
        ('Pending', '待确认'),
        ('Confirmed', '已确认'),
        ('Cancelled', '已取消'),
        ('Completed', '已完成')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name="挂号预约ID", help_text="挂号预约ID")
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, null=False, blank=False,
                               related_name='appointment', verbose_name='医生', help_text='医生')
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='appointment', verbose_name='患者', help_text='患者')
    appointment_time = models.DateTimeField(null=True, blank=True,
                                            verbose_name='预约时间', help_text='预约时间')
    # appointment_date = models.DateField(null=False, blank=False, verbose_name='预约日期', help_text='预约日期')
    # appointment_start_time = models.TimeField(null=False, blank=False, verbose_name='预约开始时间',
    #                                           help_text='预约开始时间')
    # appointment_end_time = models.TimeField(null=False, blank=False, verbose_name='预约结束时间',
    #                                         help_text='预约结束时间')
    pet_name = models.CharField(max_length=32, null=False, blank=False,
                                verbose_name="宠物名称", help_text="宠物名称")
    # 之后可以添加宠物图片，用富文本实现
    description = models.TextField(default='', null=True, blank=True,
                                   verbose_name='宠物病情描述', help_text='宠物病情描述')

    status = models.CharField(max_length=32, choices=APPOINTMENT_STATUS, default='Pending',
                              null=False, blank=False, verbose_name='预约状态', help_text='预约状态')
    comment = models.TextField(default='', null=True, blank=True,
                               verbose_name='患者评论', help_text='患者评论')

    class Meta:
        verbose_name = '宠物预约信息'
        verbose_name_plural = verbose_name
        db_table = 'pet_appointment'

    def __str__(self):
        return (f"Appointment with Dr. {self.doctor.real_name} for {self.patient.real_name} on "
                f"{self.appointment_time.strftime('%Y-%m-%d %H:%M:%S')}")
