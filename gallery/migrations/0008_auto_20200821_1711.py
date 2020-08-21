# Generated by Django 3.1 on 2020-08-21 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_auto_20200821_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='cover',
        ),
        migrations.AddField(
            model_name='gallery',
            name='last_media_upload_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
