import sys
import os
import django

sys.path.append(os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.environ["DJANGO_SETTINGS_MODULE"] = "AiPlatform.settings"

django.setup()

from management.models import Task
from management.model.yolov5 import detect


# class Detect(Thread):
#     def __init__(self, task_id=None):
#         Thread.__init__(self)
#         self.task_id = task_id
#
#     def run(self) -> None:
#         detect.run(
#             source=Task.objects.get(id=self.task_id).device.url,
#             task_id=self.task_id
#         )
#
#     def get_task_id(self):
#         return self.task_id
#
#     def update_state(self, state=None):
#         task = Task.objects.get(id=self.task_id)
#         task.state = state
#         task.save()


def run(task_id):
    detect.run(
        source=Task.objects.get(id=task_id).device.url,
        task_id=task_id
    )
