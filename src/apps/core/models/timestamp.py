from datetime import timezone
from django.conf import settings
from django.db import models


class TimeStampBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.created_at.astimezone(korean_timezone)

    @property
    def updated_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.updated_at.astimezone(korean_timezone)

    class Meta:
        abstract = True
