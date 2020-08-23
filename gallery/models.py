from django.db import models
from django.contrib.auth.models import User
from family.models import Family


# Create your models here.
class Gallery(models.Model):
    name = models.CharField(max_length=64)
    is_main = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    last_media_upload_date = models.DateTimeField(null=True, default=None)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} gallery'


class Media(models.Model):
    title = models.CharField(max_length=64)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='user_images/')
    galleries = models.ManyToManyField(Gallery)

    def __str__(self):
        return f'Media: {self.title}, upload_date: {self.upload_date}, image: {self.image.name}'


def create_gallery(name, family, is_main):
    Gallery.objects.create(
        name=name,
        family=family,
        is_main=is_main
    )