# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_leetcode.py
# @Date    : 2022/06/06:22:50
# @Author  : jinwenlong@oppo.com


# 冒泡排序
def solution1(nums):
    for i in range(len(nums)):
        flag = True
        for j in range(1, len(nums)-i):
            if nums[j-1] > nums[j]:
                nums[j-1], nums[j] = nums[j], nums[j-1]
                flag = False
        if flag:
            return


# 反转链表
class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None


def solution2(head):
    prev = None
    while head:
        temp = head.next
        head.next = prev
        prev = head
        head = temp


# 移除链表元素
def solution3(head, target):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    while head:
        if head.value == target:
            prev.next = head.next
        else:
            prev = head.next
        head = head.next


# 链表指定区间反转
def solution4(head, m, n):
    dummy = ListNode(0)
    dummy.next = head
    cur = head
    count = 1
    d = []
    while cur:
        if m <= count <= n:
            d.append(cur.val)
        if count > n:
            break
        cur = cur.next
        count += 1
    count = 1
    while head:
        if m <= count <= n:
            head.val = d.pop()
        if count > n:
            break
        head = head.next
        count += 1
    return dummy.next


if __name__ == '__main__':
    pass




