# Generated by Django 5.0 on 2024-09-06 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_remove_school_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='uuid',
            field=models.CharField(editable=False, max_length=6, unique=True),
        ),
    ]