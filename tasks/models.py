from django.db import models
from django.contrib.auth.models import User

from tasks.constants import *

status_choices = [
    (UNASSIGNED, 'unassigned'),
    (INPROGRESS, 'inprogress'),
    (DONE, 'done'),
]

class Label(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    class Meta:
        unique_together = [['name', 'owner']]
    
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completion_status = models.CharField(max_length=1, choices=status_choices, default=UNASSIGNED)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    label = models.ManyToManyField(Label, blank=True)

    def __str__(self):
        return self.title
