import asyncio
import time

now = lambda: time.time()


async def do_some_work1(x):
    while True:
        print('do_some_work1: ', time.ctime())
        await asyncio.sleep(1)
        print('do_some_work1: ', time.ctime())


async def do_some_work2(x):
    print('do_some_work2: ', time.ctime())
    await asyncio.sleep(1)
    print('do_some_work2: ', time.ctime())


async def do_some_work(x):
    print('Waiting: ', time.ctime())
    await do_some_work1(3)
    await do_some_work2(3)
    print(">>>end")


async def do_some_work83(x):
    print('doing: ', time.ctime())
    while True:
        await asyncio.sleep(1)
        print("*******", time.ctime())


start = now()

coroutine = do_some_work(2)
# coroutine2 = do_some_work83(2)
task = [coroutine, ]
asyncio.run(coroutine)

print('TIME: ', now() - start)
