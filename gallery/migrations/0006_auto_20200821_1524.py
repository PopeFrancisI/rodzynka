# Generated by Django 3.1 on 2020-08-21 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_gallery_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='cover',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
    ]
