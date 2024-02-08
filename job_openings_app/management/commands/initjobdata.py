from django.core.management.base import BaseCommand

from feed_app.models import UsefulResource
from job_openings_app.models import JobType, JobCategory, JobActivity
from job_openings_app.enums import JobType as JobTypeEnum, JobCategory as JobCategoryEnum, JobActivity as JobActivityEnum


class Command(BaseCommand):
    help = 'Initialize job data'

    def handle(self, *args, **options):
        for type_enum in JobTypeEnum:
            JobType.objects.get_or_create(name=type_enum.value)

        for category_enum in JobCategoryEnum:
            JobCategory.objects.get_or_create(name=category_enum.value)

        for activity_enum in JobActivityEnum:
            JobActivity.objects.get_or_create(name=activity_enum.value)

        resources = [
            {"name": "Министерство труда и социальной защиты РФ", "link": "https://mintrud.gov.ru/"},
            {"name": "Госуслуги.Белгородская область", "link": "https://gosuslugi31.ru/"},
            {"name": "Центр занятости населения Белгородской области", "link": "https://czn31.ru/"},
            {"name": "Министерство социальной защиты и труда Белгородской области", "link": "http://minsoc31.ru"},
            {"name": "Министерство по делам молодежи Белгородской области", "link": "http://molodchiny.ru/"},
            {"name": "Губернатор и Правительство Белгородской области", "link": "https://belregion.ru/"}
        ]
        for resource_data in resources:
            UsefulResource.objects.get_or_create(name=resource_data["name"], link=resource_data["link"])

        self.stdout.write(self.style.SUCCESS('Job data initialized successfully'))
