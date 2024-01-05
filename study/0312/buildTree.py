# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
#
# @param inorder int整型一维数组 中序遍历序列
# @param postorder int整型一维数组 后序遍历序列
# @return TreeNode类
#
from typing import List


class Solution:
    result = []

    def buildTree(self, inorder: List[int], postorder: List[int]):
        # write code here
        if postorder:
            Solution.result.append(postorder[-1])
            ind = inorder.index(postorder[-1])
            self.buildTree(inorder[:ind], postorder[:ind])
            self.buildTree(inorder[ind + 1:], postorder[ind:-1])
        return Solution.result


if __name__ == '__main__':
    print(Solution().buildTree([1,], [1,]))
