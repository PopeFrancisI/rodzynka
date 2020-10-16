from django.db import models
from django.contrib.auth.models import User
from family.models import Family


# Create your models here.
class Gallery(models.Model):
    name = models.CharField(max_length=64)
    is_main = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    last_media_upload_date = models.DateTimeField(null=True, default=None)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Media(models.Model):
    title = models.CharField(max_length=64)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='user_images/')
    galleries = models.ManyToManyField(Gallery)

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        return super().delete(keep_parents=False)

    def __str__(self):
        return f'{self.title} (upload_date: {self.upload_date.strftime("%Y-%m-%d %H:%M:%S")})'


def create_gallery(name, family, is_main, creator=None):
    gallery = Gallery.objects.create(
        name=name,
        family=family,
        is_main=is_main,
        creator=creator
    )
    return gallery
