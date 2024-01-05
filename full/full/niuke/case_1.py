"""
@Project: full
@File: case_1.py
@Author: wenlong.jin
@Time: 2023/11/29 09:42
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
堆的使用，heapq库，默认最小堆
"""
import heapq
from random import shuffle
nums = list(range(10))
shuffle(nums)
print(nums)
heapq.heapify(nums)
heapq.heappush(nums, 0.5)
heapq.heappush(nums, 3.5)
print("**"*10)
print(nums)
print(nums[0])
print(nums[1])
print(nums[2])
print(nums[3])
print("##"*10)
print(heapq.heappop(nums))
print(heapq.heappop(nums))
print(heapq.heappop(nums))
print(heapq.heappop(nums))
print("&&"*10)
print(heapq.heapreplace(nums, 3.1))
print(heapq.heappop(nums))

print("@@"*10)