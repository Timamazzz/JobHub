from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import JobOpening


@shared_task(name='archive_old_job_openings')
def archive_old_job_openings():
    # threshold_date = timezone.now() - timedelta(days=30)
    # JobOpening.objects.filter(created_at__lte=threshold_date, archived=False).update(archived=True)
    print('Iam tasks archived')

