from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    def __str__(self):
        full_name = self.first_name + " " + self.last_name
        return full_name

# Create your models here.
