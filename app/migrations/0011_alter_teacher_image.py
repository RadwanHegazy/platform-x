# Generated by Django 4.0 on 2023-07-23 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_student_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.FileField(default='static/images/default.png', upload_to='teacher-images/'),
        ),
    ]