# Generated by Django 5.0 on 2024-09-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_rename_course_name_school_upcoming_registration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footercontent',
            name='links',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='footercontent',
            name='social_media',
            field=models.JSONField(),
        ),
    ]
