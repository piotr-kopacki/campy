# Generated by Django 2.1.1 on 2018-09-09 08:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('camapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='license',
            name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='license',
            name='limit',
        ),
        migrations.RemoveField(
            model_name='license',
            name='name',
        ),
        migrations.RemoveField(
            model_name='license',
            name='price',
        ),
        migrations.AddField(
            model_name='license',
            name='type',
            field=models.CharField(choices=[('U', 'Unlimited'), ('B', 'Basic'), ('S', 'Standard'), ('P', 'Premium')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='license',
            name='purchase_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]