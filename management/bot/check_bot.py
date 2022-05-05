import time

from management.models import Task
import threading

check_arr = {}


class CheckBot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        while 1:
            try:
                global check_arr
                tasks = Task.objects.all()
                for task in tasks:
                    if len(check_arr) == 0:
                        task.state = 0
                        task.save()
                    else:
                        hit = [key for key in check_arr if key == str(task.id)]
                        task.state = 0 if len(hit) == 0 else 1
                        task.save()

            except Exception as e:
                print('check error')
                print(e)

            time.sleep(10)


def add(task_id=None, check=None):
    global check_arr
    check_arr.update({task_id: check})


def delete(task_id=None):
    global check_arr
    [check_arr[task_id].terminate() for key in check_arr if key == str(task_id)]
    del check_arr[task_id]
