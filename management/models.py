from django.db import models


# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    state = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    name = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=20)
    state = models.IntegerField(default=0)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


class Event(models.Model):
    result = models.JSONField(null=True)
    task_name = models.CharField(max_length=50, null=True)
    task_type = models.CharField(max_length=20, null=True)
    create_time = models.DateTimeField(auto_now_add=True)


class Face(models.Model):
    name = models.CharField(max_length=50)
    file_name = models.CharField(max_length=50, default='')
    url = models.CharField(max_length=500)
    face_id = models.CharField(max_length=30, default='')
