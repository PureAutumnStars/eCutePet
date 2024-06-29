from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserInfo(AbstractUser):
    # id = models.AutoField(primary_key=True, verbose_name='用户id', help_text='用户id')
    # username = models.CharField(max_length=32, db_index=True, verbose_name='用户名', help_text='用户名')
    # password = models.CharField(max_length=128, verbose_name='密码', help_text='密码')
    avatar = models.ImageField(upload_to='image/user/avatars', null=True, blank=True,
                               default='image/user/avatars/default_logo.png', verbose_name='头像', help_text='头像')
    email = models.EmailField(max_length=64, unique=True, verbose_name='邮箱', help_text='邮箱')

    is_doctor = models.BooleanField(default=False, verbose_name='是否是医生', help_text='是否是医生')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        db_table = 'user_info'

    def __str__(self):
        return self.username


UserModel = get_user_model()


class VerifyCode(models.Model):
    """
    短信验证码，用于用户注册、找回密码等
    """
    CODE_TYPE = (
        ('register', '注册'),
        ('forget', '找回密码')
    )

    code_type = models.CharField(max_length=20, default='register', choices=CODE_TYPE,
                                 verbose_name="验证码类型", help_text="验证码类型")
    code = models.CharField(max_length=10, verbose_name="验证码", help_text="验证码")
    email = models.EmailField(max_length=64, verbose_name="验证邮箱", help_text="验证邮箱")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name
        db_table = 'verify_code'


class DoctorInfo(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='doctor_info',
                                verbose_name="医生用户", help_text="医生用户")
    certificate_image_url = models.ImageField(upload_to='image/doctors/certificate', null=True, blank=True,
                                              verbose_name="职业证书照片", help_text="职业证书照片")
    certificate_number = models.CharField(max_length=32, unique=True, db_index=True,
                                          verbose_name="执业证书编号", help_text="执业证书编号")
    real_name = models.CharField(max_length=32, verbose_name="真实姓名", help_text="真实姓名")
    # 新加内容
    real_image_url = models.ImageField(upload_to='image/doctors/real_image', null=True, blank=True,
                                       verbose_name="本人真实照片", help_text="本人真实照片")

    phone_number = models.CharField(max_length=32, null=True, blank=True,
                                    verbose_name="手机号", help_text="手机号")
    ID_number = models.CharField(max_length=32, verbose_name="身份证号", help_text="身份证号")

    is_service = models.BooleanField(default=False, verbose_name='是否接诊', help_text='是否接诊')

    # 新加内容
    description = models.TextField(default='', null=True, blank=True,
                                   verbose_name="擅长领域", help_text="擅长领域")
    reception_num = models.PositiveIntegerField(default=0, verbose_name="接诊数", help_text="接诊数")
    post_num = models.PositiveIntegerField(default=0, verbose_name="发帖数", help_text="发帖数")

    class Meta:
        verbose_name = '医生额外信息'
        verbose_name_plural = verbose_name
        db_table = 'doctor_info'

    def __str__(self):
        return self.real_name
