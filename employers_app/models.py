from django.db import models

from users_app.models import User, PhoneNumberValidator


# Create your models here.
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')

    name = models.CharField(max_length=255, verbose_name="Название компании")
    inn = models.CharField(max_length=12, unique=True, verbose_name="ИНН")
    legal_address = models.TextField(verbose_name="Юридический адрес")
    contact_person_fio = models.CharField(max_length=255, verbose_name="ФИО контактного лица")

    phone_number = models.CharField(
        validators=[PhoneNumberValidator()],
        max_length=17,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )

    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    site = models.URLField(null=True, verbose_name='Сайт', blank=True)
    contact_person_email = models.EmailField(blank=True, null=True, verbose_name="Email контактного лица")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'
        app_label = 'employers_app'
