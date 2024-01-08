# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_corotine_3.py
# @Date    : 2022/07/16:22:37
# @Author  : jinwenlong@oppo.com
# # 使用for循环遇到生成器StopIteration异常不会抛出异常只会终止迭代，没有办法获得return值
def my_generator():
    for i in range(5):
        if i==2:
            return '我被迫中断了'
        else:
            yield i

# def main(generator):
#     try:
#         #不会显式触发异常，故而无法获取到return的值
#         for i in generator:
#             print(i)
#     except StopIteration as exc:
#         print("##")
#         print(exc.value)

def main(generator):
    try:
        # 使用next方法每次迭代一个值，则会显式触发StopIteration
        print(next(generator))
        print(next(generator))
        # 迭代两次以后i值为2则遇到return生成器抛出StopIteration异常
        print(next(generator))
        # 因为生成器return了触发了StopIteration异常，所以以下语句不执行
        print(next(generator))
        print(next(generator))
    except StopIteration as exc:
        # 获取返回的值
        print("##")
        print(exc.value)


# 调用
# g=my_generator()
# main(g)


# 定义一个包装“生成器”，它的本质还是生成器
def wrap_my_grnerator(generator):
    # 自动触发StopIteration异常，并且将return的返回值赋值给yield from表达式的结果，即热塑了
    result = yield from generator
    print(result)

# 调用主函数，调用的生成器是包装生成器而不是原始生成器
def main(generator):
    for i in generator:
        print(i)

g = my_generator()
wrap_g = wrap_my_grnerator(g)
# 调用
main(wrap_g)
