# Generated by Django 2.1.1 on 2018-09-09 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camapp', '0004_auto_20180909_1036'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LifeTimeLicense',
        ),
        migrations.AddField(
            model_name='camera',
            name='url',
            field=models.CharField(default='127.0.0.1', max_length=500),
            preserve_default=False,
        ),
    ]