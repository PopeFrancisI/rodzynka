from django.db import models
from django.contrib.auth.models import User
from family.models import Family


# Create your models here.
class Gallery(models.Model):
    name = models.CharField(max_length=64)
    create_date = models.DateTimeField(auto_now_add=True)
    last_media_upload_date = models.DateTimeField(null=True, default=None)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)


class Media(models.Model):
    title = models.CharField(max_length=64)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='user_images/')
    galleries = models.ManyToManyField(Gallery, null=True)


def create_gallery(name, family):
    Gallery.objects.create(
        name=name,
        family=family
    )