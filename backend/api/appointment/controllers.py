# 作   者：林枭熠
# 开发时间:2024/6/17 上午10:13
from django.db import transaction
from ninja import Query
from ninja_extra import api_controller, ControllerBase, route, exceptions, status
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from ninja_extra.ordering import Ordering, ordering
from ninja_extra.pagination import (
    paginate, PageNumberPaginationExtra, PaginatedResponseSchema
)

from api.appointment.Filter import DoctorAvailableTimeFilterSchema, AppointmentFilterSchema
from api.appointment.models import DoctorWeeklyAvailability, PatientInfo, Appointment
from api.appointment.schema import DoctorAvailableTimeSchemaIn, DoctorAvailableTimeSchemaOut, PatientSchemaOut, \
    CreateUpdatePatientSchemaIn, AppointmentDetailSchemaOut, CreateAppointmentSchemaIn, UpdateAppointmentSchemaIn, \
    DoctorAppointmentCommentSchemaOut
from api.users.models import DoctorInfo
from utils.permissions import IsDoctor


@api_controller("/appointment/doctor/available_time", tags=["doctor_available_time"])
class DoctorAvailableTimeController(ControllerBase):
    """
    医生空闲时间API，医生可以设置自己的可接诊时间
    """

    @route.post(
        "create",
        response={201: DoctorAvailableTimeSchemaOut},
        url_name="create-available-time",
        auth=JWTAuth(),
        permissions=[IsAuthenticated, IsDoctor]
    )
    @transaction.atomic
    def create_available_time(self, available_time_schema: DoctorAvailableTimeSchemaIn):
        """
        新建空闲时间，需要输入星期几，开始时间，结束时间，需要权限认证
        """
        doctor = self.get_object_or_exception(
            DoctorInfo.objects.all(),
            user=self.context.request.user,
            error_message=f"找不到你的医生信息，请联系管理员",
        )
        available_time_instance = available_time_schema.create_available_time(doctor=doctor)
        return 201, available_time_instance

    # @route.put(
    #     "/update/{str:available_time_id}",
    #     response={200: DoctorAvailableTimeSchemaOut},
    #     url_name="update-available-time",
    #     auth=JWTAuth(),
    #     permissions=[IsAuthenticated, IsDoctor]
    # )
    # @transaction.atomic
    # def update_available_time(self, available_time_id: str, available_time_schema: DoctorAvailableTimeSchemaIn):
    #     """
    #     更新医生空闲时间，需要输入星期几，开始时间，结束时间，只能更新自己的，需要权限认证
    #     """
    #     available_time_instance = self.get_object_or_exception(
    #         DoctorWeeklyAvailability.objects.all(),
    #         id=available_time_id,
    #         error_message=f"id为 {available_time_id} 的接诊时间设置不存在",
    #     )
    #     if available_time_instance.doctor.user != self.context.request.user:
    #         raise exceptions.PermissionDenied("只能更新自己的接诊时间")
    #     available_time = available_time_schema.update_available_time(available_time_instance)
    #     return 200, available_time

    @route.delete(
        "/delete/{str:doctor_id}",
        url_name="delete-all_available-time",
        response={204: dict},
        auth=JWTAuth(),
        permissions=[IsAuthenticated, IsDoctor]
    )
    @transaction.atomic
    def delete_all_available_time(self, doctor_id: str):
        """
        删除医生所有的接诊时间，需要权限认证
        """
        doctor = self.get_object_or_exception(
            DoctorInfo.objects.all(),
            id=doctor_id,
            error_message=f"id为 {doctor_id} 的医生信息找不到，请联系管理员",
        )
        if doctor.user != self.context.request.user:
            raise exceptions.PermissionDenied("只能删除自己的医生信息")
        doctor_available_times = (
            DoctorWeeklyAvailability.objects.filter(doctor=doctor)
        )
        for available_time_instance in doctor_available_times:
            available_time_instance.delete()
        return self.create_response("选中的接诊时间成功删除", status_code=status.HTTP_204_NO_CONTENT)

    @route.get(
        '',
        response=PaginatedResponseSchema[DoctorAvailableTimeSchemaOut],
        url_name="get-available-time-list",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['day_of_week', 'start_time'])
    def list_available_time(self, filters: Query[DoctorAvailableTimeFilterSchema]):
        """
        能够获取医生的空闲时间列表，并进行排序和分页，需要登录权限认证，
        搜索字段：["doctor_id", "begin_of_week", "end_of_week","start_time","end_time"]

        doctor_id：医生id (int)

        begin_of_week：星期几开始 (1-7)

        end_of_week：星期几结束 (1-7)

        start_time：开始时间 (00：00-23：59)

        end_time：结束时间 (00：00-23：59)
        """
        available_time = DoctorWeeklyAvailability.objects.all()
        available_time = filters.filter(available_time)
        return available_time


@api_controller("/appointment/patients", tags=["patients"])
class PatientsController(ControllerBase):
    """
    患者信息管理API，患者可以预约医生，需要权限认证
    """

    @route.post(
        "create",
        response={201: PatientSchemaOut},
        url_name="create-patient_info",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def create_patient(self, patient_schema: CreateUpdatePatientSchemaIn):
        """
        新建患者信息，需要权限认证，输入姓名，手机号，身份证号，需要权限认证
        """
        patient_instance = patient_schema.create_patient(user=self.context.request.user)
        return 201, patient_instance

    @route.put(
        "/update/{uuid:patient_id}",
        response={200: PatientSchemaOut},
        url_name="update-patient_info",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def update_available_time(self, patient_id: str, patient_schema: CreateUpdatePatientSchemaIn):
        """
        更新患者信息，只能更新自己的，需要权限认证
        """
        patient_instance = self.get_object_or_exception(
            PatientInfo.objects.all(),
            id=patient_id,
            error_message=f"id为 {patient_id} 的患者信息不存在",
        )
        if patient_instance.user != self.context.request.user:
            raise exceptions.PermissionDenied("只能更新自己的患者信息")
        patient = patient_schema.update_patient(patient_instance)
        return 200, patient


@api_controller("/appointment", tags=["appointment"])
class AppointmentController(ControllerBase):
    """
    挂号预约医生API，患者可以预约医生，需要权限认证
    """

    @route.post(
        "create/{str:doctor_id}",
        response={201: AppointmentDetailSchemaOut},
        url_name="create-appointment",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def create_appointment(self, appointment_schema: CreateAppointmentSchemaIn, doctor_id: str):
        """
        新建预约信息，需要权限认证，输入预约日期、预约时间、宠物名和病情描述，需要权限认证
        """
        doctor = self.get_object_or_exception(
            DoctorInfo.objects.all(),
            id=doctor_id,
            error_message=f"id为 {doctor_id} 的医生信息不存在",
        )
        if self.context.request.user.patient is None:
            raise exceptions.NotFound("未发现患者信息，请先建立患者信息")
        patient = self.context.request.user.patient
        appoint_instance = appointment_schema.create_appointment(patient=patient, doctor=doctor)
        return 201, appoint_instance

    @route.put(
        "/update/{uuid:appointment_id}",
        response={200: AppointmentDetailSchemaOut},
        url_name="update-appointment",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @transaction.atomic
    def update_appointment(self, appointment_id: str, appointment_schema: UpdateAppointmentSchemaIn):
        """
        更新就诊预约信息，只能更新自己的，需要权限认证

        当预约状态为Pending（待确认）时： 患者可以更改预约信息，也可取消预约，在预约的时间的1天前自动变为已确认

        当预约状态为Confirmed（已确认）时： 患者不能更改预约信息，在接诊结束后变为Completed（已完成）

        当预约状态为Canceled（已取消）时： 患者再也不能更改任何预约信息

        当预约状态为Completed（已完成）时： 患者只能更改评论信息comment，其它信息不能更改，同时医生接诊量reception_count+1
        """

        appointment_instance = self.get_object_or_exception(
            Appointment.objects.all(),
            id=appointment_id,
            error_message=f"id为 {appointment_id} 的就诊预约信息不存在",
        )
        if appointment_instance.patient.user != self.context.request.user:
            raise exceptions.PermissionDenied("只能更新自己的就诊预约信息")
        if appointment_instance.status == "Confirmed":
            raise exceptions.PermissionDenied("已确认的就诊预约信息不能更改")
        elif appointment_instance.status == "Canceled":
            raise exceptions.PermissionDenied("已取消的就诊预约信息不能更改")
        elif appointment_instance.status == "Completed":
            if appointment_schema.pet_name or appointment_schema.description or appointment_schema.status:
                raise exceptions.PermissionDenied("已完成的就诊预约信息不能更改")
            appointment = appointment_schema.update_appointment(appointment_instance)
            return 200, appointment
        else:  # Pending
            if appointment_schema.comment is not None:
                raise exceptions.PermissionDenied("待确认的就诊预约信息不能发布评论信息")
            appointment = appointment_schema.update_appointment(appointment_instance)
            return 200, appointment

    @route.get(
        '',
        response=PaginatedResponseSchema[AppointmentDetailSchemaOut],
        url_name="get-appointment-list",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    @ordering(Ordering, ordering_fields=['appointment_time', 'doctor__id', 'patient__id', 'status'])
    def list_appointment(self, filters: Query[AppointmentFilterSchema]):
        """
        能够获取医生或者患者的预约信息列表，并进行排序和分页，需要登录权限认证
        搜索字段：["doctor_id", "patient_id", "status", "start_time","end_time"]

        doctor_id: 医生id

        patient_id: 患者id

        status：预约状态信息 (Pending, Confirmed, Canceled, Completed)

        start_time：开始时间 (%Y-%m-%d %H:%M:%S)

        end_time：结束时间 (%Y-%m-%d %H:%M:%S)
        """

        appointments = Appointment.objects.all()
        appointments = filters.filter(appointments)
        return appointments

    @route.get(
        "/{uuid:appointment_id}",
        response=AppointmentDetailSchemaOut,
        url_name="get-one-appointment-detail",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    def retrieve_appointment(self, appointment_id: str):
        """
        输入预约的id，获取预约的详情，只能获取自己或自己的患者的预约情况
        """
        appointment_instance = self.get_object_or_exception(
            Appointment.objects.all(),
            id=appointment_id,
            error_message=f"id为 {appointment_id} 的预约信息不存在",
        )
        if appointment_instance.patient.user != self.context.request.user \
                and appointment_instance.doctor.user != self.context.request.user:
            raise exceptions.PermissionDenied("只能获取自己的接诊预约信息")
        return appointment_instance

    @route.get(
        'comment/{str:doctor_id}',
        response=PaginatedResponseSchema[DoctorAppointmentCommentSchemaOut],
        url_name="retrieve-doctor-appointment-comment",
        auth=JWTAuth(),
        permissions=[IsAuthenticated]
    )
    @paginate(PageNumberPaginationExtra, page_size=10)
    def retrieve_doctor_comment(self, doctor_id: str):
        """
        能够获取医生信息，和该医生的接诊预约评论信息，需要登录
        """
        doctor = self.get_object_or_exception(
            DoctorInfo.objects.all(),
            id=doctor_id,
            error_message=f"id为 {doctor_id} 的医生信息不存在",
        )
        return doctor
