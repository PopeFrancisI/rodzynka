from django.db import models
from django.contrib.auth.models import User
from family.models import Family


# Create your models here.
class Gallery(models.Model):
    name = models.CharField(max_length=64)
    create_date = models.DateTimeField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    cover = models.ImageField()


class Media(models.Model):
    title = models.CharField(max_length=64)
    upload_date = models.DateTimeField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    galleries = models.ManyToManyField(Gallery)


