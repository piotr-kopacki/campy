# Generated by Django 2.1.1 on 2018-09-13 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camapp', '0008_auto_20180910_2154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='url',
            new_name='rtsp',
        ),
    ]