# 作   者：林枭熠
# 开发时间:2024/6/11 下午6:26
from datetime import datetime
from datetime import timedelta
from typing import Type, List, Optional, Any

from ninja_extra.controllers import RouteContext
from typing_extensions import Self
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from ninja_extra import exceptions, service_resolver
from ninja_schema import ModelSchema, Schema  # model_validator
from pydantic import field_validator, model_validator
from api.users.models import DoctorInfo, VerifyCode

UserModel = get_user_model()


class GroupSchema(ModelSchema):
    """
    用于返回Group的Schema
    """

    class Config:
        model = Group
        include = ["name"]


class RegisterVerifyCodeSchemaIn(ModelSchema):
    """
    用于用户注册验证码的输入Schema
    """

    class Config:
        model = VerifyCode
        include = ["email"]

    @classmethod
    @field_validator("email")
    def validate_unique_email(cls, value_data: str) -> str:
        if UserModel.objects.filter(email__icontains=value_data).exists():
            raise exceptions.ValidationError("邮箱已被注册")
        return value_data

    def create(self, **kwargs) -> Type[VerifyCode]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return VerifyCode.objects.create(**_data)


class RegisterUserSchemaIn(ModelSchema):
    """
    用于用户注册的输入Schema
    """
    verify_code: str

    class Config:
        model = UserModel
        include = ["username", "email", "password"]

    @classmethod
    @field_validator("username")
    def validate_unique_username(cls, value_data: str) -> str:
        if UserModel.objects.filter(username__icontains=value_data).exists():
            raise exceptions.ValidationError("用户名已存在")
        return value_data

    @classmethod
    @field_validator("email")
    def validate_unique_email(cls, value_data: str) -> str:
        if UserModel.objects.filter(email__icontains=value_data).exists():
            raise exceptions.ValidationError("邮箱已被注册")
        return value_data

    @model_validator(mode="after")
    def validate_verify_code(self) -> Self:
        if not VerifyCode.objects.filter(code__exact=self.verify_code, email__exact=self.email).exists():
            raise exceptions.ValidationError("验证码错误")
        verify_code_instance = VerifyCode.objects.get(code__exact=self.verify_code, email__exact=self.email)
        if verify_code_instance.add_time < timezone.now() - timedelta(minutes=5):
            # verify_code.delete()
            raise exceptions.ValidationError("验证码已过期")
        else:
            return self

    def create(self, **kwargs) -> Type[UserModel]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        _data.pop("verify_code")
        return UserModel.objects.create_user(**_data)


class RegisterUserSchemaOut(ModelSchema):
    """
    用于用户注册的输出Schema
    """

    class Config:
        model = UserModel
        include = ["id", "username", "email", "is_doctor"]


class RegisterDoctorSchemaIn(ModelSchema):
    """
    用于医生用户注册的输入Schema
    """
    user: RegisterUserSchemaIn

    class Config:
        model = DoctorInfo
        include = ["ID_number", "real_name", "certificate_number", "user"]

    @classmethod
    @field_validator("ID_number")
    def validate_unique_ID_number(cls, value_data: str) -> str:
        if DoctorInfo.objects.filter(ID_number__icontains=value_data).exists():
            raise exceptions.ValidationError("身份证号码已被注册")
        return value_data

    @classmethod
    @field_validator("certificate_number")
    def validate_unique_certificate_number(cls, value_data: str) -> str:
        if DoctorInfo.objects.filter(certificate_number__icontains=value_data).exists():
            raise exceptions.ValidationError("执业证号码已被注册")
        return value_data

    def create(self, **kwargs) -> Type[DoctorInfo]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return DoctorInfo.objects.create(**_data)


class RegisterDoctorSchemaOut(ModelSchema):
    """
    用于医生用户注册的输出Schema
    """
    user: RegisterUserSchemaOut

    class Config:
        model = DoctorInfo
        include = ["id", "ID_number", "real_name", "certificate_number", "user"]


class UserUpdateSchemaIn(ModelSchema):
    """
    用于用户修改信息的输入Schema
    """

    class Config:
        model = UserModel
        include = ["avatar"]
        optional_fields = ["avatar"]

    # 更新用户信息
    def update_user(self, instance: Any, **kwargs: Any) -> Any:
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DoctorUpdateSchemaIn(ModelSchema):
    """
    用于医生用户修改信息的输入Schema
    """

    class Config:
        model = DoctorInfo
        include = ["certificate_image_url", "real_image_url", "phone_number", "is_service", "description"]
        optional_fields = ["certificate_image_url", "real_image_url", "phone_number", "is_service", "description"]

    # 更新医生信息
    def update_doctor(self, instance: Any, **kwargs: Any) -> Any:
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserRetrieveOutSchema(ModelSchema):
    """
    用于返回单个用户信息的Schema
    """
    groups: List[GroupSchema]

    @field_validator("avatar")
    def avatar_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        return context.request.build_absolute_uri(value_data)

    class Config:
        model = UserModel
        include = ["id", "username", "email", "is_doctor", "is_active", "avatar"]
        optional_fields = ["email"]


class DoctorRetrieveSchemaOut(ModelSchema):
    """
    用于返回单个医生部分信息的Schema，主要用于正常用户查看的医生信息
    """

    @field_validator("real_image_url")
    def real_image_url_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        return context.request.build_absolute_uri(value_data)

    class Config:
        model = DoctorInfo
        include = ["id", "real_name", "real_image_url", "phone_number", "ID_number", "is_service",
                   "description", "reception_num", "post_num"]


class DoctorRetrieveDetailSchemaOut(ModelSchema):
    """
    用于返回单个医生详细信息的Schema，主要用于医生查看自己的信息，和患者查看自己的医生信息
    """

    @field_validator("certificate_image_url")
    def certificate_image_url_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        return context.request.build_absolute_uri(value_data)

    @field_validator("real_image_url")
    def real_image_url_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        return context.request.build_absolute_uri(value_data)

    class Config:
        model = DoctorInfo
        include = "__all__"


class UserTokenOutSchema(Schema):
    """
    用于返回用户信息+token的Schema
    """
    user: UserRetrieveOutSchema  # 用户信息
    doctor: Optional[DoctorRetrieveDetailSchemaOut] = None  # 医生信息
    token: str  # 登录token
    token_exp_date: Optional[datetime]  # token过期时间


class EnableDisableUserINSchema(Schema):
    """
    用于启用/禁用用户，或者是删除用户的Schema
    """
    user_id: str
    _user = None

    @classmethod
    @field_validator("user_id")
    def validate_user_id(cls, value):
        user = UserModel.objects.filter(id=value).first()
        if user:
            cls._user = user
            return value
        raise exceptions.NotFound("无效的用户ID")

    def update(self):
        """
        启用/禁用用户
        """
        self._user.is_active = not self._user.is_active
        self._user.save()
        return self._user

    def delete(self):
        """
        删除用户
        """
        _id = self._user.pk
        self._user.delete()
        return _id


class EnableDisableUserOutSchema(Schema):
    """
    用于返回启用/禁用用户，或者是删除用户的Schema
    """
    message: str


class UserNameSchema(ModelSchema):
    class Config:
        model = UserModel
        include = ["id", "username"]
