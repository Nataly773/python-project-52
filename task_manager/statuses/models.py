from django.db import models


# Create your models here.
from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # для новых записей

    def __str__(self):
        return self.name

# Create your models here.
