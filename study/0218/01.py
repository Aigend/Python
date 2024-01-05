# class Animal:
#
#     def eat(self, *args):
#         print(type(self))
#         print("Animal")
#
#
# class Dog(Animal):
#
#     pass
#
# Dog().eat()

class Tree(object):
    def __init__(self, name):
        self.name = name
        self.cate = "plant"

    def __getattribute__(self, *args, **kwargs):
        print(args)
        if args[0] == "大树":
            print("log 大树")
            return "我爱大树"
        else:
            return object.__getattribute__(self, *args, **kwargs)


aa = Tree("大树")
print(aa.name)
print(aa.cate)
