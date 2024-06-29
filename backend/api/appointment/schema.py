# 作   者：林枭熠
# 开发时间:2024/6/17 上午10:13
from typing import Type, Any, List

from ninja_extra import service_resolver
from ninja_extra.controllers import RouteContext
from ninja_schema import ModelSchema
from pydantic import Field, field_validator

from api.appointment.models import DoctorWeeklyAvailability, Appointment, PatientInfo
from api.users.models import DoctorInfo
from api.users.schema import DoctorRetrieveDetailSchemaOut


class CreateUpdatePatientSchemaIn(ModelSchema):
    """
    用于患者填写或更改个人信息时的schema
    """

    class Config:
        model = PatientInfo
        include = ["real_name", "ID_number", "phone_number"]

    def create_patient(self, **kwargs: Any) -> Type[PatientInfo]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return PatientInfo.objects.create(**_data)

    def update_patient(self, instance: Any, **kwargs: Any) -> Any:
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PatientSchemaOut(ModelSchema):
    """
    用于患者查看自己个人信息的schema
    """

    class Config:
        model = PatientInfo
        include = ["id", "real_name", "ID_number", "phone_number"]


class DoctorAvailableTimeSchemaIn(ModelSchema):
    """
    用于医生用户创建自己可预约的空闲时间的schema
    """
    day_of_week: int = Field(..., ge=1, le=7)

    class Config:
        model = DoctorWeeklyAvailability
        include = ["day_of_week", "start_time", "end_time"]

    def create_available_time(self, **kwargs: Any) -> Type[DoctorWeeklyAvailability]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return DoctorWeeklyAvailability.objects.create(**_data)

    # # 更新可预约时间
    # def update_available_time(self, instance: Any, **kwargs: Any) -> Any:
    #     if not instance:
    #         raise Exception("Instance is required")
    #     data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
    #     data.update(kwargs)
    #     for attr, value in data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class DoctorAvailableTimeSchemaOut(ModelSchema):
    """
    用于医生用户展示可预约的空闲时间的schema
    """

    class Config:
        model = DoctorWeeklyAvailability
        include = ["id", "day_of_week", "start_time", "end_time"]


class CreateAppointmentSchemaIn(ModelSchema):
    """
    用于患者填写预约信息时的schema
    """

    class Config:
        model = Appointment
        include = ["appointment_time", "pet_name", "description"]

    def create_appointment(self, **kwargs: Any) -> Type[Appointment]:
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return Appointment.objects.create(**_data)


class UpdateAppointmentSchemaIn(ModelSchema):
    """
    用于患者修改预约信息时的schema
    """

    class Config:
        model = Appointment
        include = ["pet_name", "description", "comment", "status"]

    def update_appointment(self, instance: Any, **kwargs: Any) -> Any:
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_unset=True)  # 排除未修改的字段，确保了只有指定的字段会被更新
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AppointmentDetailSchemaOut(ModelSchema):
    """
    用于医生或者患者查看自己预约信息时的schema，非常详细
    """
    patient: PatientSchemaOut
    doctor: DoctorRetrieveDetailSchemaOut

    class Config:
        model = Appointment
        include = "__all__"


class AppointmentCommentSchemaIn(ModelSchema):
    """
    用于评价信息时的schema
    """

    class Config:
        model = Appointment
        include = ["id", "appointment_time", "comment"]


class DoctorAppointmentCommentSchemaOut(ModelSchema):
    """
    用于查看医生接诊的预约订单的评价信息，只有医生的相关信息和所有评价信息，没有患者信息
    """
    comment_list: List[AppointmentCommentSchemaIn] = []

    def resolve_comment_list(self, obj):
        queryset = Appointment.objects.filter(doctor__id=self.id, status="Completed")
        return queryset

    @field_validator("real_image_url")
    def real_image_url_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        return context.request.build_absolute_uri(value_data)

    class Config:
        model = DoctorInfo
        include = ["id", "real_name", "real_image_url", "phone_number", "ID_number", "is_service",
                   "description", "reception_num", "post_num"]
