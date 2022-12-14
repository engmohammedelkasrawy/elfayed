# Generated by Django 4.0.5 on 2022-08-04 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_lesson_video_lesson_video_id'),
        ('student', '0010_alter_registervideo_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField(default=1)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.branch')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_lesson', to='student.student')),
            ],
        ),
    ]
