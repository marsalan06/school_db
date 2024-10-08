# Generated by Django 5.0 on 2024-09-06 07:42

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_alter_school_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='top_bar_notifications',
            field=models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, help_text='Dictionary of notifications for the top bar'),
        ),
    ]
