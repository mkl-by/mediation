# Generated by Django 2.1.5 on 2019-01-30 17:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20190129_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='data_exit',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
