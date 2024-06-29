# 作   者：林枭熠
# 开发时间:2024/6/10 下午8:30
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from ninja_extra import api_controller, route, ControllerBase, status, exceptions
from ninja_extra.ordering import ordering, Ordering
from ninja_extra.pagination import (
    paginate, PageNumberPaginationExtra, PaginatedResponseSchema
)
from ninja_extra.permissions import IsAuthenticated, IsAdminUser
from ninja_jwt import schema
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import TokenObtainSlidingController
from ninja_jwt.tokens import SlidingToken

from utils.permissions import IsDoctor
from utils.verifycode import VerifyCode
from .models import DoctorInfo
from .schema import RegisterUserSchemaIn, UserTokenOutSchema, EnableDisableUserOutSchema, \
    EnableDisableUserINSchema, RegisterUserSchemaOut, RegisterDoctorSchemaIn, RegisterDoctorSchemaOut, \
    DoctorUpdateSchemaIn, DoctorRetrieveDetailSchemaOut, DoctorRetrieveSchemaOut, RegisterVerifyCodeSchemaIn, \
    UserRetrieveOutSchema, UserUpdateSchemaIn
from .tasks import send_register_email

User = get_user_model()


@api_controller("/verify_email", tags=["verify_email"])
class VerifyEmailController(ControllerBase):
    """
    用于验证邮箱的API控制器
    """

    @route.post(
        "/register",
        response={200: dict},
        url_name="register-verify-email"
    )
    def send_register_verify_email(self, register_email_schema: RegisterVerifyCodeSchemaIn):
        """
        用于发送注册验证邮件，需要传注册的邮箱号，无需认证
        """
        # 发送注册验证邮件
        verify_code = VerifyCode().generate_verifycode(length=6, only_number=False)
        send_register_email.delay(register_email_schema.email, verify_code)
        register_email_schema.create(code=verify_code)
        return 200, {"message": "验证码已发送至邮箱，请查收"}


@api_controller("/users", tags=["users"])
class UserController(ControllerBase):
    """
    用于用户管理的API控制器
    """

    @route.post(
        "/register",
        response={201: RegisterUserSchemaOut},
        url_name="register-user",
    )
    @transaction.atomic
    def register_user(self, user_schema: RegisterUserSchemaIn):
        """
        用于用户注册，创建用户信息，无需认证
        """
        # 创建用户
        instance = user_schema.create(is_doctor=False)
        return 201, instance

    @route.put(
        "/update/{int:pk}",
        response={200: UserRetrieveOutSchema},
        url_name="user-update",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    def update_user(self, pk: int, user_schema: UserUpdateSchemaIn):
        """
        用于更新普通用户信息，只能更改自己的信息，需要权限认证
        """
        user_instance = self.get_object_or_exception(
            User.objects.all(),
            id=str(pk),
            error_message=f"id为 {pk} 的用户不存在"
        )
        if user_instance.user != self.context.request.user:
            raise exceptions.PermissionDenied("您只能修改自己的信息")
        user = user_schema.update_user(user_instance)
        return 200, user

    @route.put(
        "/enable-disable/{int:pk}",
        response={200: EnableDisableUserOutSchema},
        url_name="enable-disable-user",
        auth=JWTAuth(),
        permissions=[IsAuthenticated, IsAdminUser]
    )
    def enable_disable_user(self, pk: int):
        """
        用于启用或禁用用户，被禁用的用户无法登录，只有管理员可以执行
        """
        user_schema = EnableDisableUserINSchema(user_id=str(pk))
        user_schema.update()
        return 200, EnableDisableUserOutSchema(message="操作成功")

    @route.get(
        "{int:pk}",
        response=UserRetrieveOutSchema,
        url_name="get-one-detail-user",
    )
    def retrieve_user(self, pk: int):
        """
        获取单个用户详细信息，不包含个人敏感信息，不需要登录，可以获得他人信息
        """
        user_instance = self.get_object_or_exception(
            User.objects.all(),
            id=str(pk),
            error_message=f"id为 {pk} 的用户不存在"
        )
        return user_instance

    @route.delete(
        "/delete/{int:pk}",
        response={204: dict},
        url_name="delete-user",
        auth=JWTAuth(),
        permissions=[IsAuthenticated, IsAdminUser]
    )
    def delete_user(self, pk: int):
        """
        用于删除用户，只有管理员可以执行
        """
        user_schema = EnableDisableUserINSchema(user_id=str(pk))
        user_schema.delete()
        return self.create_response("用户删除成功", status_code=status.HTTP_204_NO_CONTENT)


@api_controller("/doctors", tags=["doctors"])
class DoctorController(ControllerBase):
    @route.post(
        "/register",
        response={201: RegisterDoctorSchemaOut},
        url_name="doctor-register",
    )
    @transaction.atomic
    def register_doctor(self, doctor_schema: RegisterDoctorSchemaIn):
        """
        用于医生用户注册，创建用户和医生信息，无需认证
        """
        # 先创建用户
        user_instance = RegisterUserSchemaIn.create(doctor_schema.user, is_doctor=True)
        # 创建医生信息
        doctor_instance = doctor_schema.create(user=user_instance)

        return 201, doctor_instance

    @route.put(
        "/update/{int:pk}",
        response={200: DoctorRetrieveDetailSchemaOut},
        url_name="doctor-update",
        auth=JWTAuth(),
        permissions=[IsAuthenticated, IsDoctor]
    )
    def update_doctor(self, pk: int, doctor_schema: DoctorUpdateSchemaIn):
        """
        用于更新医生用户信息，只有医生可以执行，只能更改自己的信息，需要权限认证
        """
        doctor_instance = self.get_object_or_exception(
            DoctorInfo.objects.all(),
            id=str(pk),
            error_message=f"id为 {pk} 的医生不存在"
        )
        if doctor_instance.user != self.context.request.user:
            raise exceptions.PermissionDenied("您只能修改自己的信息")
        doctor = doctor_schema.update_doctor(doctor_instance)
        return 200, doctor

    @route.get(
        "",
        response=PaginatedResponseSchema[DoctorRetrieveSchemaOut],
        url_name="get-doctors-list",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['is_service'])
    def list_doctor(self):
        """
        获取所有医生信息列表，不包含医生敏感信息，需要用户权限，需要登录，默认按is_service排序
        """
        queryset = DoctorInfo.objects.all()
        return queryset

    @route.get(
        "{int:pk}",
        response=DoctorRetrieveDetailSchemaOut,
        url_name="get-one-detail-doctor",
        auth=JWTAuth(),
        permissions=[IsAuthenticated, IsDoctor | IsAdminUser]
    )
    def retrieve_doctor(self, pk: int):
        """
        获取单个医生详细信息，包含医生敏感信息，需要用户医生权限，需要登录，只能获得自己的信息
        """
        doctor_instance = self.get_object_or_exception(
            DoctorInfo.objects.all(),
            id=str(pk),
            error_message=f"id为 {pk} 的医生不存在"
        )
        if doctor_instance.user != self.context.request.user:
            raise exceptions.PermissionDenied("您只能查看自己的医生信息")
        return doctor_instance


@api_controller("/auth", tags=["auth"])
class UserTokenController(TokenObtainSlidingController):
    auto_import = True

    @route.post(
        "/login",
        response=UserTokenOutSchema,
        url_name="login"
    )
    def obtain_token(self, user_token: schema.TokenObtainSlidingSerializer):
        """
        用于用户登录，返回个人信息和token，token有效期为5h，刷新token有效期为1day，无需认证
        """
        user = user_token._user
        token = SlidingToken.for_user(user)
        doctor_info = DoctorInfo.objects.filter(user=user).first()
        return UserTokenOutSchema(
            user=user,
            doctor=doctor_info,
            token=str(token),
            token_exp_date=datetime.fromtimestamp(token["exp"])  # 时间戳转日期，不使用utc时间
            # token_exp_date=datetime.fromtimestamp(token["exp"], timezone.get_current_timezone())
        )

    @route.post(
        "/token-refresh",
        response=schema.TokenRefreshSlidingSerializer,
        url_name="refresh"
    )
    def refresh_token(self, refresh_token: schema.TokenRefreshSlidingSchema):
        """
        用于刷新token，返回刷新后的token，刷新token有效期为1day，无需认证
        """
        refresh = schema.TokenRefreshSlidingSerializer(**refresh_token.dict())
        return refresh
