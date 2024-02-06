from rest_framework import permissions
from users_app.enums import UserRoleEnum


class IsApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == UserRoleEnum.APPLICANT.value


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == UserRoleEnum.EMPLOYER.value
