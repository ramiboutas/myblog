from django.utils import timezone


def one_hour_from_now():
    return timezone.now() + timezone.timedelta(hours=1)
