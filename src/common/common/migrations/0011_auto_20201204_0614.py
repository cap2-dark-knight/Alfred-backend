# Generated by Django 3.1.3 on 2020-12-04 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_profile_alart_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='alart_time',
        ),
        migrations.AddField(
            model_name='profile',
            name='alart_times',
            field=models.IntegerField(default=512),
        ),
    ]
