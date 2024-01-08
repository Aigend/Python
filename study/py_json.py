
"""
什么是 JSON ？
JSON 指的是 JavaScript 对象表示法（JavaScript Object Notation）
JSON 是轻量级的文本数据交换格式
JSON 独立于语言：JSON 使用 Javascript语法来描述数据对象，但是 JSON 仍然独立于语言和平台。
JSON 解析器和 JSON 库支持许多不同的编程语言。 目前非常多的动态（PHP，JSP，.NET）编程语言都支持JSON。
JSON 具有自我描述性，更易理解
1、json.dumps()和json.loads()是json格式处理函数（可以这么理解，json是字符串）
　　(1)json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
　　(2)json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）
"""

import json

data = {'name': 'jack'}
print(type(data))
# 转字符串
data = json.dumps(data)
print(type(data))
# 转字典
data = json.loads(data)
print(type(data))

# 将json信息写到文件中
file = open(r'json_temp_03.text', 'w', encoding="utf-8")
json.dump(data, file)

# 读取json信息
file = open('json_temp_03.text', 'r', encoding="utf-8")
info = json.load(file)
print(info)