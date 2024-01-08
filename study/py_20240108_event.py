"""
threading.Event()
通过threading.Event()可以创建一个事件管理标志，该标志（event）默认为False，event对象主要有四种方法可以调用：

event.wait(timeout=None)：调用该方法的线程会被阻塞，如果设置了timeout参数，超时后，线程会停止阻塞继续执行；
event.set()：将event的标志设置为True，调用wait方法的所有线程将被唤醒
event.clear()：将event的标志设置为False，调用wait方法的所有线程将继续被阻塞
event.isSet()：判断event的标志是否为True
"""
import threading
import time

event = threading.Event()

def light():
    print('红灯正亮着')
    time.sleep(3)
    event.set() # 模拟绿灯亮

def car(name):
    print('车%s正在等绿灯' % name)
    event.wait() # 模拟等绿灯的操作，此时event为False,直到event.set()将其值设置为True,才会继续运行
    print('车%s通行' % name)

if __name__ == '__main__':
    # 红绿灯
    t1 = threading.Thread(target=light)
    t1.start()
    # 车
    for i in range(3):
        t = threading.Thread(target=car, args=(i,))
        t.start()
