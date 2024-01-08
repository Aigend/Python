python:
    bytes和bytearray,大小端模式：
        https://blog.csdn.net/u013008795/article/details/88945733
	线程锁:
	    https://z.itpub.net/article/detail/DE03B9C2CC0ECD3366C7ADCDE9550CE6
	元类，__new__的执行顺序：
	    https://blog.csdn.net/weixin_43988680/article/details/123903473
	python终端编码问题解决
        https://www.zybuluo.com/wzhang1117/note/803061
	pyenv 配置多版本的python环境:
	    https://www.jianshu.com/p/8aaf2525fa80
        https://blog.51cto.com/u_14320361/2488888
	ctypes库：
	    https://docs.python.org/zh-cn/3.7/library/ctypes.html#arrays
	一个强大的命令行解析器Plumbum:
	    https://www.jianshu.com/p/e13fd0c38acf
	psutil库:
	    http://www.360doc.com/content/21/1112/16/51091873_1003876985.shtml
	queue中task_done和join用法：Python queue模块详解 - lincappu - 博客园
	for 和迭代器对象、可迭代对象的关系：
		Python学习之:一文搞懂 for 和迭代器对象、可迭代对象的关系，以及他们各自的用处_for语句产生的可迭代对象为空_暖仔会飞的博客-CSDN博客
	ThreadPoolExecutor的submit和map使用:http://c.biancheng.net/view/2627.html
	python中Base64原理和使用:python中Base64原理和使用
	hashlib的使用:进行数据账号加密和完整性验证：
		https://blog.csdn.net/dreaming_coder/article/details/108247249
	asyncio教程:https://www.liujiangblog.com/course/python/83
		api:https://docs.python.org/zh-cn/3.9/library/asyncio-task.html#task-object
		https://www.jianshu.com/p/6d582b07c65a
	抽象基类，six模块的作用，直接继承和虚拟子类：
		Python高级:了解Python ABC(抽象基类)及 应用场景_hurt--的博客-CSDN博客
	requests post请求data和json数据格式深入：知乎 - 有问题，就会有答案


redis:
	中文官网：https://www.redis.com.cn/redis-stream.html

git：
	官网：https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%8F%98%E5%9F%BA


jenkins
	教程参考：https://www.bilibili.com/video/BV19M4y1c7m4
	官网：https://www.jenkins.io/zh/

grpc:
	grpc| python 实战 grpc:https://www.jianshu.com/p/43fdfeb105ff


java
	java泛型：https://blog.csdn.net/qq_66912832/article/details/125272259

kafka:
	文档：https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
	使用介绍：kafka实战教程(python操作kafka)，kafka配置文件详解_kafka python_腾讯数据架构师的博客-CSDN博客

mqtt:
	MQTT协议基础：https://www.51cto.com/article/670429.html
	MQTT深入：https://blog.csdn.net/CM_STC89C52/article/details/122712188
	python调用mqtt:https://blog.csdn.net/weixin_41656968/article/details/80848542#13subscribe

Mysql:
	MySQL为什么要用B+树实现索引:
		https://cloud.tencent.com/developer/article/1543335

docker:
	在用：https://yeasy.gitbook.io/docker_practice/image/build
	参考官网：https://docs.docker.com/engine/reference/commandline/
	中文参考网站：
	  https://yeasy.gitbook.io/docker_practice/image/dockerfile
	  https://outmanzzq.github.io/2019/10/22/docker-network/#%E4%BA%8C%E9%BB%98%E8%AE%A4%E7%BD%91%E7%BB%9C
	视频教程：https://www.bilibili.com/video/BV1og4y1q7M4?p=2
	docker-compose教程(安装，使用, 快速入门)_pushiqiang的博客-CSDN博客

can 通信：
	知乎 - 有问题，就会有答案
	https://blog.csdn.net/weixin_45403142/article/details/120075619
	https://blog.csdn.net/LiuXF93/article/details/113729294

boost库实现python和C通信：
	教程：Boost库学习与应用_翔底的博客-CSDN博客
	# 官方网站
		https://www.boost.org/
		# 下载地址
		https://www.boost.org/users/download/
		# 预编译版本下载地址
		https://sourceforge.net/projects/boost/files/boost-binaries/
		wget https://boostorg.jfrog.io/artifactory/main/release/1.73.0/source/boost_1_73_0.tar.bz2 --no-check-certificate
		tar xvf boost_1_73_0.tar.bz2
		cd boost_1_73_0
		./boostrap.sh
		./b2 --buildtype=complete install

modbus:
	半双工通信：数据可以在一个信号载体的两个方向上传输，但是不能同时传输
	例如，在一个局域网上使用具有半双工传输的技术，一个工作站可以在线上发送数据，然后立即在线上接收数据，
	这些数据来自数据刚刚传输的方向。 
	像全双工传输一样，半双工包含一个双向线路（线路可以在两个方向上传递数据）

uWSGI服务器：https://blog.csdn.net/Aifore/article/details/86703685
    https://blog.csdn.net/baidu_24752135/article/details/123726280
 uWSGI：
  uWSGI是应用服务器，是一个应用执行的容器。应用服务器往往也会集成 HTTP Server 的功能，但是不如专业的 HTTP Server 那么强大，所以应用服务器往往是运行在 HTTP Server 的背后
 WSGI:
  WSGI 是一种 Web 服务器网关接口。WSGI，全称 Web Server Gateway Interface，或者 Python Web Server Gateway Interface ，是为 Python 语言定义的 Web 服务器 和 Web 应用程序或框架之间的一种简单而通用的接口。自从 WSGI 被开发出来以后，许多其它语言中也出现了类似接口。

  它是一 个 Web 服务器（如 nginx，uWSGI 等服务器）与 web 应用（如用 Flask 框架写的程序）通信的一种 规范。WSGI协议其实是定义了一种server与application解耦的规范，即可以有多个实现WSGI server的服务器，也可以有多个实现WSGI application的框架，那么就可以选择任意的server和application组合实现自己的web应用。例如uWSGI和Gunicorn都是实现了WSGI server协议的服务器，Django，Flask是实现了WSGI application协议的web框架，可以根据项目实际情况搭配使用。
 uwsgi
  同WSGI一样是一种通信协议，uWSGI是实现了uwsgi和WSGI两种协议的Web服务器

reset和rebase的区别
为什么git add和git commit要分开操作

在python函数参数中，*和**的区别

udp和tcp的区别
http和tcp的关系
http和https的区别，说了加密的过程，又问了https的证书，如何防止攻击？
get和post的区别，既然功能差不多，post存在的意义，幂等操作等

项目里python+django的部署是怎么做的，用了哪些技术，如何通信等
项目里涉及到的多线程/多进程
线程和进程的区别，python多线程，GIL
python多继承时，调用父类同一个方法的先后顺序
python怎么定义类中的静态方法
面向对象的三个基本要素，具体讲一下

.py和.pyc文件有什么区别？
	.py 文件是 Python 源代码文件，包含了 Python 程序的源代码，以及解释器需要执行程序的其他信息。
	.pyc 文件是 Python 编译后的字节码文件，它包含了被编译成机器码的 Python 程序。
	在 Python 中，当你导入一个模块时，解释器会自动查找该模块的 .pyc 文件，
	如果找到了就会直接执行 .pyc 文件中的字节码。
	如果找不到 .pyc 文件，就会先将 .py 文件编译成 .pyc 文件，然后再执行 .pyc 文件。
	这样做的目的是为了提高程序的执行效率，因为执行字节码的速度要快于执行源代码。
	 但是，.pyc 文件只能在相同的操作系统和 Python 版本下使用，如果操作系统或者 Python 版本不同就会出现问题。

python相关知识，迭代器、生成器、装饰器？
metaclass、args、kwargs。Flask与wsgi是如何交互的？
Flask源码读过么？Flask的IO多路复用用在了什么地方？

什么是闭包?
	闭包就是外部函数中定义一个内部函数，内部函数引用外部函数中的变量，外部函数的返回值是内部函数;

装饰器是一种增加函数或类功能的简单方法，它可以快速给不同的函数或类插入相同的功能。语法：“@装饰器名”加在函数之前

什么是生成器和迭代器？它们之间有什么区别？
迭代器
作用：简化循环的代码并可以节约内存
是一个可以记住遍历的位置的对象。迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退
生成器
作用：节约大量内存
生成器(generator)的定义与普通函数类似，生成器使用yield关键字生成值。
使用了 yield 的函数被称为生成器、生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器
原理：在调用生成器运行的过程中，每次遇到 yield 时函数会暂停并保存当前所有的运行信息，返回 yield 的值, 并在下一次执行 next() 方法时从当前位置继续运行

Python垃圾回收机制
python采用的是引用计数机制为主，标记-清除和分代收集(隔代回收、分代回收)两种机制为辅的策略
计数机制：Python的GC模块主要运用了引用计数来跟踪和回收垃圾。在引用计数的基础上，还可以通过“标记-清除”解决容器对象可能产生的循环引用的问题。通过分代回收以空间换取时间进一步提高垃圾回收的效率。
标记-清除：：标记-清除的出现打破了循环引用，也就是它只关注那些可能会产生循环引用的对象
缺点：该机制所带来的额外操作和需要回收的内存块成正比。
隔代回收
原理：将系统中的所有内存块根据其存活时间划分为不同的集合，每一个集合就成为一个“代”，垃圾收集的频率随着“代”的存活时间的增大而减小。也就是说，活得越长的对象，就越不可能是垃圾，就应该减少对它的垃圾收集频率。那么如何来衡量这个存活时间：通常是利用几次垃圾收集动作来衡量，如果一个对象经过的垃圾收集次数越多，可以得出：该对象存活时间就越长。

浅拷贝，	
	改变原始对象中为可变类型的元素的值，会同时影响拷贝对象；
	改变原始对象中为不可变类型的元素的值，不会响拷贝对象。
深拷贝，
	除了顶层拷贝，还对子元素也进行了拷贝。经过深拷贝后，原始对象和拷贝对象所有的可变元素地址都没有相同的了

map()函数将给定函数应用于可迭代对象(列表、元组等)，然后返回结果(map对象)。
我们还可以在map()函数中，同时传递多个可迭代对象。 
numbers = (1, 2, 3, 4)
result = map(lambda x: x + x, numbers)
print(list(result))

reduce()函数接受一个函数和一个序列，并在计算后返回数值。
from functools import reduce
a = lambda x,y:x+y
print(reduce(a,[1,2,3,4]))


解释re模块的split()、sub()、subn()方法？
split()：只要模式匹配，此方法就会拆分字符串。
sub()：此方法用于将字符串中的某些模式替换为其他字符串或序列。
subn()：和sub()很相似，不同之处在于它返回一个元组，将总替换计数和新字符串作为输出
import re
string = "There are two ball in the basket 101"
re.split("\W+",string)
---------------------------------------
['There', 'are', 'two', 'ball', 'in', 'the', 'basket', '101']
re.sub("[^A-Za-z]"," ",string)
----------------------------------------
'There are two ball in the basket    '
re.subn("[^A-Za-z]"," ",string)
-----------------------------------------
('There are two ball in the basket    ', 10)

Python中OOPS是什么？
面向对象编程，抽象(Abstraction)、封装(Encapsulation)、继承(Inheritance)、多态(Polymorphism)

什么是Python中的猴子补丁？
猴子补丁(monkey patching)，是指在运行时动态修改类或模块
from SomeOtherProduct.SomeModule import SomeClass
def speak(self):
    return "Hello!"
SomeClass.speak = speak

zip函数获取可迭代对象，将它们聚合到一个元组中，然后返回结果。
zip()函数的语法是zip(*iterables)
numbers = [1, 2, 3]
string = ['one', 'two', 'three'] 
result = zip(numbers,string)
print(set(result))
-------------------------------------
{(3, 'three'), (2, 'two'), (1, 'one')}

# 1.5个python标准库
# os, date,datetime,re,math,re,sys,
#
# 2.匿名函数lambda的使用
# lambda x, y: x*y；函数输入是x和y，输出是它们的积x*y
# lambda:None；函数没有输入参数，输出是None
# lambda *args: sum(args); 输入是任意个数的参数，输出是它们的和(隐性要求是输入参数必须能够进行加法运算)
# lambda **kwargs: 1；输入是任意键值对参数，输出是1
# filter函数。此时lambda函数用于指定过滤列表元素的条件。
# 例如filter(lambda x: x % 3 == 0, [1, 2, 3])指定将列表[1,2,3]中能够被3整除的元素过滤出来，其结果是[3]。
# sorted函数。此时lambda函数用于指定对列表中所有元素进行排序的准则。
# 例如sorted([1, 2, 3, 4, 5, 6, 7, 8, 9], key=lambda x: abs(5-x))将列表[1, 2, 3, 4, 5, 6, 7, 8, 9]
# 按照元素与5距离从小到大进行排序，其结果是[5, 4, 6, 3, 7, 2, 8, 1, 9]

py gevent学习

import time

import gevent
from gevent import monkey
monkey.patch_all()


def f1(n):
    for i in range(n):
        print(gevent.getcurrent(), i)
        gevent.sleep(1)

def f2(n):
    for i in range(n):
        print(gevent.getcurrent(), i)


def f3(n):
    for i in range(n):
        print(gevent.getcurrent(), i)

print("********")
g1 = gevent.spawn(f1, 5)
print("------")
g2 = gevent.spawn(f2, 5)
print("#####")
g3 = gevent.spawn(f3, 5)
print("&&&")
print("^^^^^")
g1.join()
gevent.sleep(10)
print("@@@")
g2.join()
print("%%%")
g3.join()

# gevent.joinall([g1,g2, g3])

print("******************")

import gevent
from gevent import monkey
import urllib.request
monkey.patch_all()


def downloader(file_name, url_address):
    req = urllib.request.urlopen(url_address)
    content = req.read()
    with open(file_name, "wb") as f:
        f.write(content)


def main():
    gevent.joinall([
        gevent.spawn(downloader, "绝地求生女解说Corrine宅个人Vlog视频.mp4",
                                 "https://img.dongyoutu.com/20210423/841dd2e192db6c70630ba12112c386f8.mp4"),
        gevent.spawn(downloader, "《跑跑卡丁车：RUSH+》与《绝地求生Mobile》一起联手推出搞笑视频.mp4", "https://img.dongyoutu.com/20210402/1111.mp4")
                    ])


if __name__ == '__main__':
    main()


class MyMeta(type):

    def __new__(cls, *args, **kwargs):
        print("mymeta __new__ ...")
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, class_name, class_bases, class_dic):
        print("mymeta __init__ ...")
        print(self)
        print(class_bases)
        print(self.__bases__)
        print(class_dic)
        if '__doc__' not in class_dic or len(class_dic['__doc__'].strip(' \n')) == 0:
            raise TypeError('类中必须有文档注释，并且文档注释不能为空')


    # def __call__(self, *args, **kwargs):
    #     print("mymeta __call__ ...")


class People(metaclass=MyMeta):
    """

    """
    def __new__(cls, *args, **kwargs):
        print("people __new__ ...")
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        print("people __init__ ...")

    def __call__(self, *args, **kwargs):
        print("people __call__ ...")


# 同步和异步：用来描述任务的提交方式
# 同步：任务提交之后，原地等待任务的返回结果
# 异步：任务提交之后，不再等待结果，而是去做其他事情

# 阻塞和非阻塞：描述进程的运行状态
# 阻塞：阻塞态
# 非阻塞：就绪和运行态，cpu利用率较高

# 同步阻塞
# 同步非阻塞
# 异步阻塞
# 异步非阻塞：目前很多的异步框架都是支持的

# 创建进程，方式很多
"""
1.os.fork()  # windows系统不支持
2.multiprocessing
3.subprocess  # 运维使用，用来执行终端代码，功能不多
"""
from multiprocessing import Process, current_process
import time
import os
age = 18
def func(name):
	print(f"任务{current_process().pid}执行中")
	print(f"任务{os.getpid()}执行中")
	print(f"父进程{os.getppid()}执行中")

	time.sleep(5)
	age = 16

# linux 查看进程 ps aux |  grep pid
# windows 查看进程 tasklist | findstr pid

# 这里推荐使用if判断的方式创建，因为windows系统和linux系统不同，
# linux 创建的时候会把函数执行的代码，和数据集全部都拷贝一份
# linux 创建的时候会把当前模块再进行一次导包，如果不加if 会进入死循环
if __name__ == "__main__":
	p = Process(target=func, args=("写讲话稿", ))
	p.start()  # 异步提交任务：提交后不会等待任务的结果
	# p.terminate() # kill -9 pid ，taskkill pid, 这里发起系统调用，杀死进程
	# p.is_alive() # 如果调用terminate后立刻调用is_alive会获取不到理想的结果，系统杀死进程需要时间，延迟0.001s
	print("主进程")
	p.join()
	print(age) # 这里会打印18,主进程和子进程数据是隔离的

# 创建进程的第二种方式，通过类的方式

class MyProcess(Process):

	def __init__(self, name):
		super().__init__()
		self.task_name = name

	def run():
		pass

if __name__ == "__main__":
	p = MyProcess("约会")
	p.start()
	p.join()  # 等待子进程执行结束，才继续往下执行
	print("主进程") # 不加join ,默认会等子进程结束，程序才完成


# 僵尸进程：
	子进程结束后，会有一些资源占用（进程号，进程运行状态，运行时间等）等待父进程通过系统调用回收
	除了init进程之外，所有的进程，最后都会进入僵死进程

	视频这里介绍主进程代码执行结束，子进程代码还未结束时，主进程会等待回收子系统资源
	实际测试发现，主进程代码执行完，子进程代码还未执行完时，主进程仍存在

	危害：
		子进程退出之后，父进程没有及时处理，僵死进程会一直占用计算机资源 
		如果产生了大量的僵死进程，系统资源占用，没有可用的进程号，导致系统产生新的进程
# 孤儿进程：
	子进程处于存活状态，但是父进程意外死亡，比如：终端中把父进程杀死掉，没有人回收子系统资源
	操作系统会开设一个孤儿院（init进程）,用来管理孤儿进程，回收孤儿进程的资源

# 守护进程：
	p.daemon = True # 这个设置要在p.start()之前配置，否则报错，主进程结束，子进程也结束
# 互斥锁
from multiprocessing import Lock 
import random
def search_tickeet(name):
	with open('data/tickets', 'r', encoding='utf-8') as f:
		dic = json.load(f)
		print(f"用户{name}查询余票，还剩{dic.get('tickets_num')}")	


def buy_ticket(name):
	with open('data/tickets', 'r', encoding='utf-8') as f:
		dic = json.load(f)
	time.sleep(random.randint(1, 5))
	if dic.get('tickets_num') > 0:
		dic['tickets_num'] -= 1
		with open('data/tickets', 'w', encoding='utf-8') as f:
			json.dump(dic, f)
		print(f"{name} 买票成功")
	else：
		print(f"余票不足，{name} 买票失败")

def task(name, mutex):
	search_tickeet(name)
	mutex.acquire()
	buy_ticket(name)
	mutex.release()

if __name__ == "__main__"":
	mutex = Lock()
	for i in range(9):
		p = Process(target=task, args=(i, mutex))
		p.start()

# 行锁
# 表锁
# 锁把并发变成串行，会造成互锁问题






# 第一种使用方法
import queue
queue.Queue()
# 第二种使用方法
from multiprocessing import queues
queues.Queue()
# 第三种用法
from multiprocessing import Queue
q = Queue(6)  # maxsize 消息队列最大保存的消息数目
		  # 不传值，默认为326767
# 队列是先进先出
q.put('a')
q.put('b')
q.put('c')
q.put('d')
q.put('e')
q.put('f')

print(q.full()) # 判断队列是否满了

q.put('h')  # 存第个元素的时候程序阻塞
q.put_nowait('h')  # raise Full 报错，queue.Full
q.put('h', timeout=3)  # 3s之内还是满的，会报错

v1 = q.get()
print(v1)
v2 = q.get()
v3 = q.get()
v4 = q.get()
v5 = q.get()
v6 = q.get()

print(q.empty())

v7 = q.get()  # 阻塞，什么时候有数据，继续往下执行
v7 = q.get_nowait()  # 无数据报错 raise Empty _queue.Empty
v7 = q.get(timeout=3) # 无数据等待3s,3s后仍无数据就报错

"""
q.put()
q.get()
q.full()
q.empty()
q.put_nowait()
q.get_nowait()
这四个函数在多进程极限条件下可能不太准确，这个进程刚满了，存数据报错，下一个进程可能就取了数据
"""

池的概念：
	保证计算机硬件安全，最大限度的利用计算机的资源，降低了程序的运行效率，也保证了计算机硬件的安全

进程池
线程池

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
pool=ThreadPoolExecutor()
		max_workers = min(32, (os.cpu_count() or 1) + 4) # 开设的线程数

pool.submit(fn, /, *args, **kwargs) # submit是异步提交

	#如果你想要函数的调用者在某个参数位置只能使用位置参数而不能使用关键字参数传参，那么你只需要在所需位置后面放置一个/
	def f1(a, *, b, c):
	#希望强迫调用者使用某些参数，且必须以关键字参数的形式传参，那么你只需要在所需位置的前一个位置放置一个*

同步提交：提交之后，原地等待任务的结果
异步提交：任务提交之后不等待，继续往下执行
线程池和信号量的区别：
	信号量是锁，线程是自己创建的，控制线程的执行，阻塞
	线程池是由线程池创建线程，控制线程的数量

不等待任务的返回结果，怎么获取方法的返回结果

 
import gevent
gevent.monkey_patch_all()
import time
def test(name):
    for i in range(100):
        time.sleep(1)
        print(name, i)
def run():
    gevent.spawn(test, "aaa")
    gevent.spawn(test, "bbb")
    time.sleep(50)
g = spawn(run)
print("***")
g.join()



# 多道技术：
  # 目的:让单核实现并发效果
  # 核心：切换+保存状态
  # cpu 切换分2种情况：
  	# 1.当一个程序遇到IO操作的时候，操作系统会剥夺该程序cpu的执行权限
  	# 2.当一个程序长时间占用CPU的时候，操作系统会剥夺该程序cpu的执行权限
  # 允许多个应用程序同时进入内存，cpu交替执行
  	# 当一道程序因为IO暂停运行时，CPU便会去立即运行另一道程序，如：
	#   	程序A CPU在运行时，磁盘是空闲的，是可以允许另一个程序B读取进入内存的
	#   	如果程序A CPU运行完毕，在输出的过程，CPU闲置下来，是可以运行程序B的
# 并发和并行：
  # 单核不能实现并行，但是可以实现并发

# 进程调度

	1. 先来先服务算法
	2. 短作业优先调度算法
	3. 时间片轮转和多级反馈机制

	进程的状态图：

	创建---《提交》---就绪
		IO完成由阻塞进入就绪；时间片完由运行进入就绪；系统调度由就绪进入运行
		阻塞----《IO请求》----运行---《释放》----终止

# CS BS 架构
# 连接问题：
	多系统：手机，电脑，智能家居
	多介质：wifi, 有线
	目标问题：具体设备
	多软件同时使用网络

	光纤：光信号
	网线：电信号
	wifi:电磁波信号
# OSI 七层模型
应用层：程序：微信
表示层：用来描述文件类型的，如果不告诉你发的数据类型，你无法使用正确的程序打开
会话层：数据拆包，数据拆包合并，决定什么时候开始发，什么时候开始断

传输层：解决用什么方式发的问题：tcp和udp协议
		tcp 可靠，传输速度慢，经过的设备多，发生丢包的可能性大：发生100M，会拆分成很多的小包 1500 byte 0001 0002 每发一个包都要进行确认
		udp 不可靠 速度快，经过的设备少，丢包的可能性小：直播平台使用
		端口的概念：数据都是通过网卡发送的 通过端口确认包是发给哪个程序的
网络层：解决发到哪里的问题：ip地址
		公网ip  全世界唯一， 快递地址
		内网ip  局域网唯一， 房间号

数据链路层：解决发给谁的问题：mac地址，每块网卡都有，全世界唯一，根据mac地址可以查询具体厂商的网卡
物理层：解决信号转换的问题：网线会把数字信号转成电信号，光纤会转成光信号

TCP/IP协议：规定数据的组织形式
协议：头部+数据
打包的过程就是给数据加头部，拆包的过程就是给数据拿掉头部
物理层：
	01100001010110 
	规定：一组数据称之为一个bit流
数据链路层
	如果都是01信号，无法分组，我们就无法解析数据
	以太网协议规定：一组数据称之为一个数据帧
	mac地址占6个字节 IP协议类型占2个字节，为了数据的正确传输，最后结尾会有4个字节的帧校验
	6+6+2+4 = 18 有的人说14,有的说18一个意思
	以太网的数据长度是46-1500 Byte，超过1500就会进行切片
	以太网帧格式：
	前导码(7Byte) + 帧起始界定符SFD(1Byte) + 源mac地址(6Byte) + 目的mac地址(6Byte) + 类型(2Byte) + 数据(46-1500Byte) + 帧校验/帧尾FCS(4Byte)
	工作方式：广播
	不能把全世界所有的电脑都集中到一个广播域中，就有了网络层
	局域网计算机 通过网关(网关有两个地址，一个局域网地址，一个对外地址)
		网关收到数据，使用路由协议(规定公网上设备收到数据后应该发给下面哪个设备)把数据往公网发
网络层
	IPV4:0.0.0.0---255.255.255.255 大约43亿设备，不够用
		NAT技术：内网IP段
			10.0.0.0---10.255.255.255 一千六百多万
			172.16.0.0---12.31.255.255 104万
			192.168.0.0---192.168.255.255 65536个

		172.0.0.0-127.255.255.255 保留地址
	IPV6:
		分为8组。每组4个16进制数，128个bit

	子网掩码：和IPV4 ip地址相同
		2种形式：192.168.3.88/255.255.255.0
			linux：192.168.3.88/24
		通过IP地址和子网掩码就可以知道局域网的IP范围，进而判断对方的IP是否是在自己的网段范围内
		如果不是同一个网段，需要跨子网通信，就把数据发送给网关，网关走路由协议，通过IP地址把数据发给对方子网
			是同一个网段，就通过mac地址通信

	ARP 协议：
		交换机如果只知道对方的ip地址不知道mac地址的时候，ARP 广播给局域网内所有机器，目的ip会回应mac地址

		arp -a 
		arp -d * 清空当前的arp表
传输层
	mac地址是局域网通信
	(源mac地址， 目的mac/网关mac) (源ip 目的ip) 数据
	TCP/UDP
	tcp头部+数据/udp头部+数据
	头部：包含源端口，目的端口， tcp还包括数据段的序列号
	传输层数据比较大的时候，会拆分成段

	DNS 用的就是udp传输

	握手包标识：SYN
	挥手包标识：FIN
	数据包标识：PSH
	确认包标识：ACK
	重发包标识：RST
	紧急包标识：URG
	三次握手：
	1.客户端---》服务端：SYN seq=x, ack（抓包看第一次是没有ack的）
		我们抓包看到的seq有可能是0，这是以为waireshark做了转换，修改下工具配置可以看到这个随机数
	2.服务端---》客户端：ACK, seq=y, ack=x+1
		到这里，客户端就知道了和服务端的通信是通畅的，但服务端不知道和客户端是否通信OK
	3.服务端---》客户端：SYN, seq=y, ack=x+1
	4.客户端---》服务端：ACK seq=x+1, ack=y+1
	2和3往往是一起发送的

	四次挥手：
	1.客户端---》服务端：FIN seq=x, ack=y
	2.服务端---》客户端：ACK, seq=y, ack=x+1
	3.服务端---》客户端：FIN,ACK seq=y, ack=x+1
	4.客户端---》服务端：ACK seq=x+1, ack=y+1


	SYN 洪水攻击
		客户端状态：CLOSED --- SYN_SENT --- ESTABLISHED
		服务端状态：LISTEN ---  SYN_RCVD --- ESTABLISHED

	DHCP协议：

应用层
wireshark:
	ip.addr == 192.168.1.3

