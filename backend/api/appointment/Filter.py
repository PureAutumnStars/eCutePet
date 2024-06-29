# 作   者：林枭熠
# 开发时间:2024/6/17 下午2:49
from datetime import datetime, time
from typing import Optional

from django.db.models import Q
from ninja import FilterSchema
from pydantic import Field


class DoctorAvailableTimeFilterSchema(FilterSchema):
    """
    医生设定的可预约时间Schema，用于医生查看自己的可预约时间设置
    """
    # 医生ID
    doctor_id: Optional[int] = Field(None, q=['doctor__id__icontains'])
    # 星期几开始
    begin_of_week: Optional[int] = None
    # 星期几结束
    end_of_week: Optional[int] = None
    # 开始时间
    start_time: Optional[time] = None
    # 结束时间
    end_time: Optional[time] = None

    def filter_begin_of_week(self, value: bool) -> Q:
        return Q(day_of_week__gte=self.begin_of_week) if value else Q()

    def filter_end_of_week(self, value: bool) -> Q:
        return Q(day_of_week__lte=self.end_of_week) if value else Q()

    def filter_start_time(self, value: bool) -> Q:
        return Q(start_time__gte=self.start_time) if value else Q()

    def filter_end_time(self, value: bool) -> Q:
        return Q(end_time__lte=self.end_time) if value else Q()


class AppointmentFilterSchema(FilterSchema):
    """
    就诊预约的过滤Schema，用于医生和患者查看自己的预约信息
    """
    # 预约状态
    status: Optional[str] = Field(None, q=['status__icontains'])
    # 医生id
    doctor_id: Optional[int] = Field(None, q=['doctor__id__exact'])
    # 患者id
    patient_id: Optional[int] = Field(None, q=['patient__id__exact'])
    # 开始时间
    start_time: Optional[datetime] = None
    # 结束时间
    end_time: Optional[datetime] = None

    def filter_start_time(self, value: bool) -> Q:
        return Q(appointment_time__gte=self.start_time) if value else Q()

    def filter_end_time(self, value: bool) -> Q:
        return Q(appointment_time__lte=self.end_time) if value else Q()
