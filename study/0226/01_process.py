from multiprocessing import Process
import time
import os


def func():
    print(f"***{os.getpid()}***")
    print(f"###{os.getppid()}")
    time.sleep(1000)


if __name__ == "__main__":
    p = Process(target=func, )
    p.daemon = True
    p.start()
    time.sleep(20)
    print(f"主进程:{os.getpid()}")
