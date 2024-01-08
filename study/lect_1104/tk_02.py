#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/11/4 10:31
import tkinter as tk

root = tk.Tk()
textLabel = tk.Label(master=root, text="大家好,才是真的好.",  # 载入文本
                   justify=tk.LEFT,  # 声明文本的位置
                font=("楷体", 20),  # 声明文本字体
                 fg="white")
textLabel.pack()
root.mainloop()
