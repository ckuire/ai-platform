# Generated by Django 3.2.5 on 2022-04-15 09:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_event_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
