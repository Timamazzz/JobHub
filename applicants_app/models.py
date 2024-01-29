from django.db import models

from users_app.models import User, PhoneNumberValidator


# Create your models here.
class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')

    fio = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="ФИО"
    )

    birth_date = models.DateField(
        blank=True, null=True,
        verbose_name="Дата рождения"
    )

    phone_number = models.CharField(
        validators=[PhoneNumberValidator()],
        max_length=17,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )

    email = models.EmailField(unique=True, blank=False, null=False, verbose_name="Email")

    resume = models.TextField(
        blank=True, null=True,
        verbose_name="Резюме"
    )
