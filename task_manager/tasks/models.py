from django.db import models
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name="tasks"
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_tasks"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="executed_tasks",
        null=True,
        blank=True
    )
    labels = models.ManyToManyField(Label, related_name="tasks", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)