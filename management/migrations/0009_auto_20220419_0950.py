# Generated by Django 3.2.5 on 2022-04-19 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_event_create_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='device',
            name='url',
            field=models.CharField(max_length=500),
        ),
    ]