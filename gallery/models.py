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
    upload_date = models.DateTimeField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    galleries = models.ManyToManyField(Gallery)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.galleries:
            galleries = self.galleries.all()
            for gallery in galleries:
                gallery.last_image_upload_date = self.upload_date

        super(Media, self).save(self, force_insert=False, force_update=False, using=None,
             update_fields=None)


def create_gallery(name, family):
    Gallery.objects.create(
        name=name,
        family=family
    )