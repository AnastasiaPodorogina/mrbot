from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    count = models.fields.IntegerField(default=0)
