# Generated by Django 3.1.3 on 2020-12-04 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_profile_alart_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='alart_time',
        ),
    ]