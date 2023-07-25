# Generated by Django 4.0 on 2023-07-25 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('level', models.CharField(choices=[('1 ث', '1 ث'), ('2 ث', '2 ث'), ('3 ث', '3 ث')], max_length=100)),
                ('final_mark', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=500)),
                ('image', models.FileField(default='default.png', upload_to='teacher-images/')),
                ('wa_number', models.URLField(default='')),
                ('is_online', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('paid_at', models.DateField(blank=True, null=True)),
                ('expired_at', models.DateField(blank=True, null=True)),
                ('teacher_uuid', models.CharField(blank=True, max_length=10000, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('code', models.IntegerField()),
                ('parent_phone', models.URLField()),
                ('level', models.CharField(choices=[('1 ث', '1 ث'), ('2 ث', '2 ث'), ('3 ث', '3 ث')], max_length=100)),
                ('student_uuid', models.CharField(max_length=1000)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('name', models.IntegerField()),
                ('paid_date', models.DateField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.teacher'),
        ),
    ]
