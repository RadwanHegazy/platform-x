# Generated by Django 4.0 on 2023-07-25 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='teacher',
        ),
    ]
