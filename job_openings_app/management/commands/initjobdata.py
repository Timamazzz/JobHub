from django.core.management.base import BaseCommand
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

        self.stdout.write(self.style.SUCCESS('Job data initialized successfully'))
