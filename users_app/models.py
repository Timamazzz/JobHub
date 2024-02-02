from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from users_app.enums import UserRoleEnum


# Create your models here.
class PhoneNumberValidator(RegexValidator):
    regex = r'^\+?1?\d{9,15}$'
    message = 'Enter a valid phone number.'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')

        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=[(role.name, role.value) for role in UserRoleEnum],
        default=UserRoleEnum.APPLICANT.name,
        verbose_name="Роль"
    )

    #vk_login = models.CharField(max_length=255, blank=True, null=True, verbose_name="VK Login")

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username






