# Generated by Django 2.1.5 on 2019-01-29 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsmess',
            name='messages',
            field=models.TextField(blank=True, help_text='Текст может содержать 70 знаков', max_length=70, null=True),
        ),
    ]
