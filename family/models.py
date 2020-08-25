from django.contrib.auth.models import User
from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=32, unique=True)
    last_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    user = models.ManyToManyField(User)
    invitations = models.ManyToManyField(User, related_name='invited_user')