# Generated by Django 4.0.5 on 2022-07-19 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_remove_lesson_price_branch_price'),
        ('student', '0009_alter_registervideo_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registervideo',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.branch'),
        ),
    ]