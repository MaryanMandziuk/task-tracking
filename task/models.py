from django.db import models

#
class Task(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=200)
    timer = models.DurationField()
    done = models.BooleanField()
    created = models.DateField(auto_now=False, auto_now_add=True)
    finished = models.DateField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.name
