class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


    def __str__(self):
        return self.val

    def __repr__(self):
        return str(self.val)
#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
#
# @param root TreeNode类 the root of binary tree
# @return int整型二维数组
#

class Solution:

    def threeOrders(self, root: TreeNode):
        # write code here
        if not root:
            return [[], [], []]
        result = []
        front = []
        medium = []
        back = []
        self.frontOrders(root, front)
        self.mediumOrders(root, medium)
        self.backOrders(root, back)
        result.append(front)
        result.append(medium)
        result.append(back)
        return result

    def frontOrders(self, root: TreeNode, front):
        if root:
            front.append(root)
            self.frontOrders(root.left, front)
            self.frontOrders(root.right, front)

    def mediumOrders(self, root, medium):
        if root:
            self.mediumOrders(root.left, medium)
            medium.append(root)
            self.mediumOrders(root.right, medium)

    def backOrders(self, root, back):
        if root:
            self.backOrders(root.left, back)
            self.backOrders(root.right, back)
            back.append(root)

if __name__ == '__main__':
    a1=TreeNode(1)
    a2=TreeNode(2)
    a3=TreeNode(3)
    a1.left=a2
    a1.right=a3
    print(Solution().threeOrders(a1))