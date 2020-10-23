from django.contrib.auth.models import User
from django.db import models

from family.models import Family


class Wish(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True)
    is_important = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


def get_newest_wishes(family, n=5):
    """
    returns n newest family wishes
    :param family:
    :param n: number of wishes to be returned
    :return:
    """
    family: Family
    try:
        newest_wishes = family.wish_set.order_by('-create_date')[:n]
    except Exception:
        newest_wishes = None

    return newest_wishes
