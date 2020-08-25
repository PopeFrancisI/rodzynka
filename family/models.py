from django.contrib.auth.models import User
from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=32, unique=True)
    last_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    user = models.ManyToManyField(User)
    invited_users = models.ManyToManyField(User, related_name='inviting_families', blank=True)
    requesting_users = models.ManyToManyField(User, related_name='requested_families', blank=True)
