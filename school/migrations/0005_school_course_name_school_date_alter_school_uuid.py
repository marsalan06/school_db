# Generated by Django 5.0 on 2024-09-02 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_school_video_url_alter_school_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='course_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='uuid',
            field=models.CharField(default='db7c69', max_length=6),
        ),
    ]
