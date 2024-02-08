from django.core.management.base import BaseCommand
from tqdm import tqdm

from feed_app.models import UsefulResource
from job_openings_app.models import JobType, JobCategory, JobActivity, Municipality
from JobHub.enums import JobTypeEnum, JobCategoryEnum, JobActivityEnum, MunicipalityEnum


class Command(BaseCommand):
    help = 'Initialize job data'

    def handle(self, *args, **options):
        for type_enum in tqdm(JobTypeEnum, desc='Initializing Job Types'):
            JobType.objects.get_or_create(name=type_enum.value)

        for category_enum in tqdm(JobCategoryEnum, desc='Initializing Job Categories'):
            JobCategory.objects.get_or_create(name=category_enum.value)

        for activity_enum in tqdm(JobActivityEnum, desc='Initializing Job Activities'):
            JobActivity.objects.get_or_create(name=activity_enum.value)

        for municipality_enum in tqdm(MunicipalityEnum, desc='Initializing Municipalities'):
            Municipality.objects.get_or_create(name=municipality_enum.value)

        resources = [
            {"name": "Министерство труда и социальной защиты РФ", "link": "https://mintrud.gov.ru/"},
            {"name": "Госуслуги.Белгородская область", "link": "https://gosuslugi31.ru/"},
            {"name": "Центр занятости населения Белгородской области", "link": "https://czn31.ru/"},
            {"name": "Министерство социальной защиты и труда Белгородской области", "link": "http://minsoc31.ru"},
            {"name": "Министерство по делам молодежи Белгородской области", "link": "http://molodchiny.ru/"},
            {"name": "Губернатор и Правительство Белгородской области", "link": "https://belregion.ru/"}
        ]
        for resource_data in tqdm(resources, desc="Initializing resources"):
            UsefulResource.objects.get_or_create(name=resource_data["name"], link=resource_data["link"])

        self.stdout.write(self.style.SUCCESS('Job data initialized successfully'))
