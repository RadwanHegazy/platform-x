# Generated by Django 4.0 on 2023-07-26 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='password',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='username',
        ),
    ]
