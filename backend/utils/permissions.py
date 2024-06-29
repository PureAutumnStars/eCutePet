# 作   者：林枭熠
# 开发时间:2024/6/13 下午7:57
from typing import Any

from django.http import HttpRequest
from ninja_extra import permissions, ControllerBase


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request: HttpRequest, controller: "ControllerBase") -> bool:
        return True

    def has_object_permission(
            self, request: HttpRequest, controller: "ControllerBase", obj: Any
    ) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request: HttpRequest, controller: "ControllerBase") -> bool:
        return True

    def has_object_permission(
            self, request: HttpRequest, controller: "ControllerBase", obj: Any
    ) -> bool:
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class IsDoctor(permissions.BasePermission):
    """
    只允许医生用户进行的操作
    """

    def has_permission(self, request: HttpRequest, controller: "ControllerBase") -> bool:
        user = request.user or request.auth
        return request.user.is_doctor

    def has_object_permission(
            self, request: HttpRequest, controller: "ControllerBase", obj: Any
    ) -> bool:
        user = request.user or request.auth
        return request.user.is_doctor
