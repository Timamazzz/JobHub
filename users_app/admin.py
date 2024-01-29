from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User, Applicant, Employer
from .enums import UserRoleEnum


class ApplicantInline(admin.StackedInline):
    model = Applicant
    can_delete = False


class EmployerInline(admin.StackedInline):
    model = Employer
    can_delete = False


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    inlines = [ApplicantInline, EmployerInline]


admin.site.register(User, CustomUserAdmin)
