from django.contrib.auth.models import User
from django.db import models

from family.models import Family


class Wish(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True)
    is_important = models.BooleanField(default=False)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
