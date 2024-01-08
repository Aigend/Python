# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# # author:靳文龙
# # @time: 2020/4/4 0:07
#
# import requests
#
# # r=requests.get("https://static1.scrape.center/")
#
# r=requests.get('http://httpbin.org/get')
#
# print(r.text)
#
# print(type(r.text))
#
# print(r.json())
#
# print(type(r.json()))
#

#
# def reverseVowels(s: str) -> str:
#     # 字符串操作成列表
#     set_s = ("a", "e", "i", "o", "u", "A", "E", "I", "O", "U")
#     list_s = list(s)
#
# #     low = 0
# #     high = len(list_s) - 1
# #
# #     while low < high:
# #         while list_s[low] not in set_s:
# #             low += 1
# #         while list_s[high] not in set_s:
# #             high -= 1
# #         print(low, high)
# #         if low < high:
# #             list_s[low], list_s[high] = list_s[high], list_s[low]
# #             low += 1
# #             high -= 1
# #     return "".join(list_s)
# #
# # print(reverseVowels(".,"))
#
# class Solution:
#     def validPalindrome(self, s: str) -> bool:
#         # 如果收尾指针相同的话就不做判断
#         # 首尾不相同的时候，就去掉第一个，判断后面的；或者去掉最后一个，判断前面的
#         list_s = list(s)
#
#         low = 0
#         high = len(list_s) - 1
#
#         while low < high:
#             if list_s[low] != list_s[high]:
#                 print("***")
#                 if self.isPalindrom(list_s, low + 1, high) or self.isPalindrom(list_s, low, high - 1):
#                     return True
#             else:
#                 low += 1
#                 high -= 1
#
#         return True  # 首尾都相同，肯定是回文字符串
#
#     def isPalindrom(self, s, low, high) -> bool:
#         while low < high:
#             if s[low] == s[high]:
#                 low += 1
#                 high -= 1
#             else:
#                 return False
#         else:
#             return True
from typing import List


class Solution:
    def findLongestWord(self, s: str, dictionary: List[str]) -> str:

        result = ""
        for dic in dictionary:
            if len(dic) > len(result):
                if self.checkTargetWord(s, dic):  # 判断dic能否由s组成
                    result = dic
            elif len(dic) == len(result) and self.check_alha(result, dic):
                # 字母序列和大于result
                print("&&&&&&&")
                if self.checkTargetWord(s, dic):  # 判断dic能否由s组成
                    result = dic
                    print("*^^^^^^^^^^^^"+result)
        return result

    def checkTargetWord(self, s, target) -> bool:
        # 双指针,此题有个问题，字母删除的顺序和单词的顺序必须一致，如果不一致就不是这种写法
        p1, p2 = 0, 0  # 判断target是否能有s组成
        s = list(s)
        target = list(target)
        while p1 < len(s) and p2 < len(target):
            if s[p1] == target[p2]:
                p2 += 1
                if p2 == len(target):
                    return True
            p1 += 1
        else:
            return False

    def check_alha(self, m, n):
        print("****")
        print(m)
        print(n)
        for i in range(len(m)):
            if m[i] > n[i]:
                print(m[i])
                print(n[i])
                return True

            else:
                return False


print(Solution().findLongestWord("wordgoodgoodgoodbestword",["word","good","best","good"]))

print("********************************")
# print(Solution().check_alha("good","best"))
print(Solution().check_alha("best","good"))
s=[3,4,7,2,1,8,0,6]
import heapq
print(heapq.heapify(s))
print(s)
print(heapq.heappop(s))
print(heapq.heappop(s))
print(heapq.heappop(s))
print(heapq.heappop(s))
print(heapq.heappop(s))
print(heapq.heappop(s))
print(heapq.heappop(s))
print(heapq.heappop(s))
print(heapq.heappop(s))