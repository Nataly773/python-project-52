from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="tasks")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_tasks")
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="assigned_tasks", null=True, blank=True)
    labels = models.ManyToManyField(Label, blank=True, related_name="tasks")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name