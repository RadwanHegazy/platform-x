# Generated by Django 4.0 on 2023-07-20 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_exam_level_alter_result_mark_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='level',
            field=models.CharField(choices=[('1 ث', '1 ث'), ('2 ث', '2 ث'), ('3 ث', '3 ث')], max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.CharField(choices=[('1 ث', '1 ث'), ('2 ث', '2 ث'), ('3 ث', '3 ث')], max_length=100),
        ),
    ]
