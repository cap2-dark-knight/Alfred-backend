# Generated by Django 3.1.3 on 2020-12-02 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20201203_0316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='check_smartkeyword',
        ),
    ]