# Generated by Django 2.1.5 on 2019-02-04 17:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_auto_20190204_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_exit',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
