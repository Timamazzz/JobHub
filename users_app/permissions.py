from rest_framework import permissions
from users_app.enums import UserRoleEnum


class IsApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        return request.user and request.user.is_authenticated and request.user.role == UserRoleEnum.APPLICANT.name


class IsApplicantVerify(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        if request.user.is_authenticated and request.user.role == UserRoleEnum.APPLICANT.name:
            return request.user.applicant_profile.is_profile_complete()

        return False


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        return request.user and request.user.is_authenticated and request.user.role == UserRoleEnum.EMPLOYER.name
