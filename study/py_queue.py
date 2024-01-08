# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/29 19:40
# @File: py_queue.py
import queue
q = queue.Queue()
q.put('python')
q.put('-')
q.put('100')
for i in range(3):
    print("**")
    print(q.get_nowait())
    print("##")
    # q.task_done()  # 如果不执行 task_done，join 会一直处于阻塞状态，等待 task_done 告知它数据的处理已经完成
print(q.empty())
q.join()