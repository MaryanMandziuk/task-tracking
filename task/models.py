from django.db import models
from datetime import timedelta


class Task(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True)
    timer = models.DurationField(default=timedelta())
    done = models.BooleanField(default=False)
    created = models.DateField(auto_now=False, auto_now_add=True)
    finished = models.DateField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.name
