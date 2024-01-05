"""
@Project: full
@File: case_2.py
@Author: wenlong.jin
@Time: 2023/11/30 11:13
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""


def traceback(nums, start, trace):
    res.append(trace[:])  # 这里不用copy,用切片
    for i in range(start, len(nums)):
        trace.append(nums[i])
        # traceback(nums, start + 1, trace) # 这里有错
        traceback(nums, i + 1, trace)  # 这里有错
        trace.pop()


def traceback1(nums, start, trace, k):
    if len(trace) == k:
        res.append(trace[:])
    for i in range(start, len(nums)):
        trace.append(nums[i])
        traceback1(nums, i + 1, trace, k)
        trace.pop()


def traceback2(nums, start, trace):
    if len(trace) == len(nums):
        res.append(trace[:])
    for i in range(start, len(nums)):
        trace.append(nums[i])
        traceback2(nums, i + 1, trace)
        trace.pop()

# 网上标准答案
# def subsets(nums):
#     def backtrack(nums, start, track):
#         res.append(track[:])
#         for i in range(start, len(nums)):
#             track.append(nums[i])
#             backtrack(nums, i + 1, track)
#             track.pop()
#
#     track = []
#     res = []
#     backtrack(nums, 0, track)
#     return res


if __name__ == '__main__':
    res = []
    # traceback([1, 2, 3], 0, [])
    # print(res)

    # traceback1([1, 2, 3], 0, [], 2)
    # print(res)

    traceback2([1, 2, 3], 0, [])
    print(res)

    # print(subsets([1, 2, 3]))
