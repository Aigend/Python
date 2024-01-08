# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/29 21:26
# @File: py_asyncio_task.py
import asyncio
import time


async def nested():
    await asyncio.sleep(3)
    return 42


async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    print(time.ctime())
    task = asyncio.create_task(nested())
    await asyncio.sleep(1)
    print("###", time.ctime())
    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task
    print(time.ctime())


asyncio.run(main())
