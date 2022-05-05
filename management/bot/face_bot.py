import sys
import os
import django

sys.path.append(os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.environ["DJANGO_SETTINGS_MODULE"] = "AiPlatform.settings"

django.setup()

from management.model.face import detect
from management.models import Task

from threading import Thread


# class Detect(Thread):
#     def __init__(self, task_id=None):
#         Thread.__init__(self)
#         self.task_id = task_id
#
#     def run(self) -> None:
#         run_t = Thread(target=detect.run, args=(Task.objects.get(id=self.task_id).device.url,))
#         process_t = Thread(target=detect.process_frame, args=(self.task_id,))
#         run_t.start()
#         process_t.start()
#
#     def get_task_id(self):
#         return self.task_id
#
#     def update_state(self, state=None):
#         task = Task.objects.get(id=self.task_id)
#         task.state = state
#         task.save()


def run(task_id):
    run_t = Thread(target=detect.run, args=(Task.objects.get(id=task_id).device.url,))
    process_t = Thread(target=detect.process_frame, args=(task_id,))
    run_t.start()
    process_t.start()
