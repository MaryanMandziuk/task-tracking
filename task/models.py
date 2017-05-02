from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    timer = models.DurationField(default=timedelta())
    done = models.BooleanField(default=False)
    created = models.DateField(auto_now=False, auto_now_add=True)
    finished = models.DateField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.name is None:
            return ""
        return self.name

    class Meta:
        ordering = ['created', 'name']
