from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Family(models.Model):
    name = models.CharField(max_length=64, unique=True)
    last_name = models.CharField(max_length=64)
    users = models.ManyToManyField(User)
