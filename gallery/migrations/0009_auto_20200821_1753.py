# Generated by Django 3.1 on 2020-08-21 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0008_auto_20200821_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
