import face_recognition
import cv2
import numpy as np
import time
import queue

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# import os
# import sys
# import django
#
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ["DJANGO_SETTINGS_MODULE"] = "AiPlatform.settings"
# django.setup()

from management.models import Event, Task, Face

root = Path(__file__).resolve().parent

q = queue.Queue()


def run(source=None):
    video_capture = cv2.VideoCapture(source)
    while 1:
        success, frame = video_capture.read()
        if success:
            q.put(frame)
        else:
            video_capture = cv2.VideoCapture(source)
        time.sleep(1)


def process_frame(task_id=None):
    while 1:
        try:
            if not q.empty():
                frame = q.get()

                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    face_encodings, known_face_names = load_face()
                    matches = face_recognition.compare_faces(face_encodings, face_encoding)
                    face_distances = face_recognition.face_distance(face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

                if len(face_names) != 0:
                    img = draw_face(frame, face_locations, face_names)
                    file_path = root / 'results' / str(int(time.time() * 1000))
                    file_path = file_path.with_suffix('.jpg')
                    if not file_path.parent.exists():
                        file_path.parent.mkdir(parents=True)
                    cv2.imwrite(str(file_path), img)

                    face = Face.objects.get(face_id=f'{name}')
                    result = {
                        "detect_detail": [
                            f'{face.name}'
                        ],
                        "detect_image_path": [
                            ""
                        ],
                        "snapshot_image_path": file_path.parent.name + '/' + file_path.name,
                        "snapshot_mark_image_path": "",
                        "type": "face"
                    }
                    curTask = Task.objects.get(id=task_id)
                    Event(task_type=curTask.type, task_name=curTask.name, result=result).save()
        except Exception as e:
            print(e)
            pass


def load_face():
    face_images = Path(root / 'load')
    face_names = [face.stem for face in face_images.iterdir()]

    face_encodings = []
    for face in face_images.iterdir():
        face_encodings.append(
            face_recognition.face_encodings(face_recognition.load_image_file(face.resolve()))[0]
        )
    return face_encodings, face_names


def draw_face(frame, face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        return cv2ImgAddText(frame, name, left + 6, top - 6)


def cv2ImgAddText(img, text, left, top, textColor=(255, 255, 255), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "Songti.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

# run("rtsp://192.168.151.154:8554/live")
