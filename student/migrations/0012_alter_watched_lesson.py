# Generated by Django 4.0.5 on 2022-08-04 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_lesson_video_lesson_video_id'),
        ('student', '0011_watched'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watched',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson'),
        ),
    ]