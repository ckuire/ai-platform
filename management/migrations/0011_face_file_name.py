# Generated by Django 3.2.5 on 2022-04-19 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_alter_device_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='face',
            name='file_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
