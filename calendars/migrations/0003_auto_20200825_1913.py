# Generated by Django 3.1 on 2020-08-25 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_auto_20200824_2047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='date_from',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date_to',
        ),
    ]
