from django.db import models
from django.contrib.auth.models import User
from family.models import Family


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


def get_newest_media(family):
    """
    returns a tuple where first value is the newest media/image from family gallery,
    and the second value is the gallery containing that media/image.
    :param family:
    :return:
    """
    last_updated_gallery = family.gallery_set.filter(last_media_upload_date__isnull=False)\
        .order_by('-last_media_upload_date').first()
    print(last_updated_gallery)
    try:
        newest_media = last_updated_gallery.media_set.latest('upload_date')
    except Exception as e:
        print(e)
        newest_media = None
    return newest_media, last_updated_gallery


def get_newest_media_in_gallery(gallery):
    """
    returns the newest media from a gallery.
    :param gallery:
    :return:
    """
    try:
        newest_media = gallery.media_set.latest('upload_date')
    except Exception as e:
        print(e)
        newest_media = None
    return newest_media
