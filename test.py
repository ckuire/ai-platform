# from threading import Thread
# import time
# import multiprocessing
#
# class th_1(Thread):
#
#     def __init__(self):
#         Thread.__init__(self)
#
#     def run(self) -> None:
#         print('th_1 is start')
#         t = th_2()
#         t.setDaemon(True)
#         t.start()
#         print('th_1 end')
#
#
# class th_2(Thread):
#
#     def __init__(self):
#         Thread.__init__(self)
#
#     def run(self) -> None:
#         print('th_2 is start')
#         for i in range(5):
#             print(f'th_2 is runing {i}')
#             time.sleep(2)
#
#
# thread1 = th_1()
# # thread1.setDaemon(True)
# thread1.start()
#
# while 1:
#     print(thread1.is_alive())
#     time.sleep(2)
import threading

test = {}

thread1 = 'thread1'
value1 = threading.Thread()

thread2 = 'thread2'
value2 = threading.Thread()

test.update({thread1: value1, thread2: value2})
print(test)

[print(test[key]) for key in test if key == 'thread1']
