import time
import random
import multiprocessing

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Device, Task, Event, Face
from django.http import JsonResponse
from management.bot import yolov5_bot, face_bot
from .bot import check_bot
from pathlib import Path
from django.core.paginator import Paginator

PROXY_IP = '192.168.101.242'


def index(request):
    return HttpResponseRedirect('device')


def device(request):
    if request.is_ajax() and request.method == 'POST':
        optype = request.POST['optype']
        if optype == 'add':
            deviceName = request.POST['deviceName']
            deviceUrl = request.POST['deviceUrl']
            Device(name=deviceName, url=deviceUrl).save()
            return JsonResponse({"code": 200})
        elif optype == 'delete':
            deviceId = request.POST['deviceId']
            try:
                Device.objects.get(id=deviceId).delete()
            except:
                return JsonResponse({
                    "code": 500,
                    "message": "存在关联的任务，无法删除设备"
                })
            return JsonResponse({"code": 200})
        elif optype == 'update':
            device_id = request.POST['deviceId']
            device_name = request.POST['deviceName']
            device_url = request.POST['deviceUrl']
            device = Device.objects.get(id=device_id)
            device.name = device_name
            device.url = device_url
            device.save()
            return JsonResponse({"code": 200})
    devices = Device.objects.order_by('-create_time')
    return render(request, 'device.html', {'devices': devices})


def task(request):
    if request.is_ajax() and request.method == 'POST':
        optype = request.POST['optype']
        if optype == 'add':
            taskName = request.POST['taskName']
            deviceId = request.POST['deviceId']
            taskType = request.POST['taskType']
            Task(name=taskName, type=taskType, device=Device.objects.get(id=deviceId)).save()
            return JsonResponse({"code": 200})
        elif optype == 'delete':
            taskId = request.POST['taskId']
            Task.objects.get(id=taskId).delete()
            return JsonResponse({"code": 200})
        elif optype == 'start':
            task_id = request.POST['taskId']
            task = Task.objects.get(id=task_id)

            if task.type == 'yolov5':
                detect = multiprocessing.Process(target=yolov5_bot.run, args=(task_id,))
            elif task.type == 'face':
                detect = multiprocessing.Process(target=face_bot.run, args=(task_id,))

            detect.start()

            check_bot.add(task_id=task_id, check=detect)
            return JsonResponse({"code": 200})

        elif optype == 'stop':
            task_id = request.POST['taskId']
            check_bot.delete(task_id)
            return JsonResponse({"code": 200})

    tasks = Task.objects.all()
    devices = Device.objects.all()
    return render(
        request, 'task.html',
        {
            'tasks': tasks,
            'devices': devices
        }
    )


def event(request, page):
    events = Event.objects.order_by('-create_time')
    paginator = Paginator(events, 10)
    page_obj = [] if paginator.count == 0 else paginator.get_page(page)
    return render(
        request, 'event.html',
        {
            'events': page_obj,
            'server': f"http://{PROXY_IP}:12323/"
        }
    )


def face(request):
    if request.is_ajax() and request.method == 'POST':
        optype = request.POST['optype']
        if optype == 'add':
            face_name = request.POST['faceName']
            face = request.FILES['face']

            file_save_path = Path('/Users/uire/pythonProjects/AiPlatform/management/model/face/load/' + str(int(time.time() * 1000)) + ''.join(random.sample('1234567890', 6)))
            file_save_path = file_save_path.with_suffix(Path(request.FILES['face'].name).suffix)

            if not file_save_path.parent.exists():
                file_save_path.parent.mkdir(parents=True)

            with open(file_save_path, 'wb') as f:
                for line in face.readlines():
                    f.write(line)

            Face(name=face_name, file_name=face.name, face_id=file_save_path.stem, url=file_save_path.name).save()

        elif optype == 'delete':
            face_id = request.POST['faceId']
            face = Face.objects.get(id=face_id)
            face.delete()

        return JsonResponse({"code": 200})
    faces = Face.objects.all()
    return render(
        request, 'face.html',
        {
            'faces': faces,
            'server': f'http://{PROXY_IP}:12323/face_db'
        }
    )
