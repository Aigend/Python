#!/usr/bin/env python
# -*- coding:utf-8 -*-
# # author:靳文龙
# # @time: 2020/4/1 23:17
"1:将两个字符串紧挨着写在一起"
str1 = "Python教程" "http://c.biancheng.net/python/"
print(str1)
"2: str() 和 repr() 函数将数字转换为字符串"
"""
str() 用于将数据转换成适合人类阅读的字符串形式。
repr() 用于将数据转换成适合解释器阅读的字符串形式（Python 表达式的形式）
"""
"""s 本身就是一个字符串，但是我们依然使用 str() 和 repr() 对它进行了转换。
从运行结果可以看出，str() 保留了字符串最原始的样子，而 repr() 使用引号将字符串包围起来
这就是 Python 字符串的表达式形式"""
s = "http://c.biancheng.net/shell/"
s_str = str(s)
s_repr = repr(s)
print( type(s_str) )
print (s_str)
print( type(s_repr) )
print (s_repr)

"3:使用[ ]除了可以获取单个字符外，还可以指定一个范围来获取多个字符，也就是一个子串或者片段"
url = 'http://c.biancheng.net/java/'
#获取索引从3处22（不包含22）的子串
print(url[7: 22]) # 输出 zy
#获取索引从7处到-6的子串
print(url[7: -6]) # 输出 zyit.org is very
#获取索引从-7到6的子串
print(url[-21: -6])
#从索引3开始，每隔4个字符取出一个字符，直到索引22为止
print(url[3: 22: 4])

url = 'http://c.biancheng.net/java/'
#获取从索引5开始，直到末尾的子串
print(url[7: ])
#获取从索引-21开始，直到末尾的子串
print(url[-21: ])
#从开头截取字符串，直到索引22为止
print(url[: 22])
#每隔3个字符取出一个字符
print(url[:: 3])

"4:汉字在 GBK/GB2312 编码中占用 2 个字节，而在 UTF-8 编码中一般占用 3 个字节"
str1 = "人生苦短，我用Python"
# len(str1.encode('gbk'))
# len(str1.encode())

"5:字符串常用函数"
"""
str.split(sep,maxsplit) 方法可以实现将一个字符串按照指定的分隔符切分成多个子串，这些子串会被保存到列表中（不包含分隔符），作为方法的返回值反馈回来
sep：用于指定分隔符，可以包含多个字符。此参数默认为 None，表示所有空字符，包括空格、换行符“\n”、制表符“\t”等。
maxsplit：可选参数，用于指定分割的次数，最后列表中子串的个数最多为 maxsplit+1。如果不指定或者指定为 -1，则表示分割次数没有限制
"""

"""
 str.join(iterable)它是 split() 方法的逆方法，用来将列表（或元组）中包含的多个字符串连接成一个字符串
>>> list = ['c','biancheng','net']
>>> '.'.join(list)
'c.biancheng.net'
"""

"""
str.count(sub[,start[,end]])
str：表示原字符串；
sub：表示要检索的字符串；
start：指定检索的起始位置，也就是从什么位置开始检测。如果不指定，默认从头开始检索；
end：指定检索的终止位置，如果不指定，则表示一直检索到结尾
"""
str = "c.biancheng.net"
str.count('.', 1)
str.count('.',2)
str.count('.',2,-3)

"""
str.find(sub[,start[,end]])
str：表示原字符串；
sub：表示要检索的目标字符串；
start：表示开始检索的起始位置。如果不指定，则默认从头开始检索；
end：表示结束检索的结束位置。如果不指定，则默认一直检索到结尾
"""
str = "c.biancheng.net"
str.find('.',2)
#位于索引（2，-4）之间的字符串为“biancheng”，由于其不包含“.”，因此 find() 方法的返回值为 -1
str.find('.',2,-4)
#Python 还提供了 rfind() 方法，与 find() 方法最大的不同在于，rfind() 是从字符串右边开始检索
str.rfind('.')  #11

"""
str.index(sub[,start[,end]])
str：表示原字符串；
sub：表示要检索的子字符串；
start：表示检索开始的起始位置，如果不指定，默认从头开始检索；
end：表示检索的结束位置，如果不指定，默认一直检索到结尾
"""
#index() 方法也可以用于检索是否包含指定的字符串，不同之处在于，当指定的字符串不存在时，index() 方法会抛出异常
# find() 和 rfind() 一样，字符串变量还具有 rindex() 方法，其作用和 index() 方法类似，不同之处在于它是从右边开始检索
str = "c.biancheng.net"
# str.index('z')
str.rindex('.') #11

"""
startswith() 方法用于检索字符串是否以指定字符串开头，如果是返回 True；反之返回 False
endswith() 方法用于检索字符串是否以指定字符串结尾，如果是则返回 True；反之则返回 False
"""
str = "c.biancheng.net"
str.startswith("c")
str.startswith("http")
str.startswith("b", 2)
str.endswith("net")

"""
title() 方法用于将字符串中每个单词的首字母转为大写，其他字母全部转为小写，转换完成后，此方法会返回转换得到的字符串
lower() 方法用于将字符串中的所有大写字母转换为小写字母，转换完成后，该方法会返回新得到的字符串
upper() 的功能和 lower() 方法恰好相反，它用于将字符串中的所有小写字母转换为大写字母
"""
str = "c.biancheng.net"
str.title()#'C.Biancheng.Net'
str = "I LIKE C"
str.lower()#'i like c'
str = "i like C"
str.upper()#'I LIKE C'

"特殊字符，指的是制表符（\t）、回车符（\r）、换行符（\n）"
"""
字符串变量提供了 3 种方法来删除字符串中多余的空格和特殊字符，它们分别是：
strip()：删除字符串前后（左右两侧）的空格或特殊字符。
lstrip()：删除字符串前面（左边）的空格或特殊字符。
rstrip()：删除字符串后面（右边）的空格或特殊字符。
通过 strip() 确实能够删除字符串左右两侧的空格和特殊字符，但并没有真正改变字符串本身
"""
str = "  c.biancheng.net \t\n\r"
print(str.strip())
print("-------------")
print(str.strip(" ,\r"))#'c.biancheng.net \t\n'
print("-------------")
print(str)#'  c.biancheng.net \t\n\r'
print("-------------")
print(str.lstrip())#'c.biancheng.net \t\n\r'
print("-------------")
print(str.rstrip())#'  c.biancheng.net'

"""
str.format(args)
str 用于指定字符串的显示样式；args 用于指定要进行格式转换的项，如果有多项，之间有逗号进行分割
"""