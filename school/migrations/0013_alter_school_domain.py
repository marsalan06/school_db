# Generated by Django 5.0 on 2024-09-29 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_alter_footercontent_links_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='domain',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]