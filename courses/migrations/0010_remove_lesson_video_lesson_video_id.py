# Generated by Django 4.0.5 on 2022-08-04 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_branch_is_free'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='video',
        ),
        migrations.AddField(
            model_name='lesson',
            name='video_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
