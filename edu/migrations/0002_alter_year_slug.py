# Generated by Django 4.0.4 on 2022-05-21 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
