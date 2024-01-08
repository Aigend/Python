#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" python2需要在首行写-*- coding:utf-8 -*-才能支持中文，python3开始默认支持中文了，就可以省去这行注释"""
"""
linux自带python解释器。在编写.py文件时，只要写上了#!/usr/bin/python这行注释
用户就可以直接在命令行用文件名来执行py文件，例如：   testmode.py
类似于在window命令行中，你必须得写 python  testmode.py  或 javac testmode.java
 或 java testmode.class 来运行文件，你要通过文件名前面的关键字才能去启动对应的解释器
"""
"""
#!/usr/bin/python 注释的问题在于，Linux只系统默认的py解释器（也就是自带的那个）来运行文件。这样用户就无法使用自己的python版本了
#!/usr/bin/env python 的出现可则让用户可以自行选择python版本，用户可以在环境变量中配置自己的py解释器
"""
"""
推荐使用#!/usr/bin/env python 的注释，而非 #!/usr/bin/python
在windows环境中执行文件的话，这行注释就无所谓:
先定位到你py文件所在的文件夹后，再使用 python testmode.py 这样的语句来执行文件。window系统也不会去看这行注释
"""
str1 = "Python教程" "http://c.biancheng.net/python/"
print(str1)
str2 = "Java" "Python" "C++" "PHP"
print(str2)
"""----------------------------------------------"""
"""Ctrl+B，Ctrl+单击：就可以很方便的跳转到源码里的类，方法，函数，变量的定义"""
"""Ctrl+J：直接插入常用代码了"""
"""Ctrl + -符号 来收缩单函数代码，这个主要是为了方便查看"""
"""Ctrl + Shift + -符号 来收缩代码，这个主要是为了方便查看"""
class People:
    def say(self):
        print("我是一个人，名字是：",self.name)
class Animal:
    def display(self):
        print("人也是高级动物")
#同时继承 People 和 Animal 类
#其同时拥有 name 属性、say() 和 display() 方法
class Person(People, Animal):
    pass
zhangsan = Person()
zhangsan.name = "张三"
zhangsan.say()
zhangsan.display()


