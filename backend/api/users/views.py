from django.contrib.auth import get_user_model, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import redirect

# Create your views here.

UserModel = get_user_model()


# 自定义用户验证方法
class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 根据用户名或邮箱获取用户对象
            user = UserModel.objects.get(Q(username=username) | Q(email=username))
            # 验证密码，同时用户要能够登录
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception as e:
            return None
