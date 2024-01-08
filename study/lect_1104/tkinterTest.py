#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/11/4 9:27
import tkinter
from tkinter import *

def callback(event):
    frame.focus_set()
    print("clicked at:",event.x,event.y)
def key(event):
    # frame.focus_set()
    print("clicked at:",event.char)
def closeWindow(event):
    if tkinter.messagebox.askokcancel("quit","afhkakfaf"):
        pass

root =Tk()
frame = Frame(root,width=100,height=80)
frame.bind('<Button-1>',callback)
frame.bind('<Key>',key)
frame.pack()
frame.focus_set()

root.protocol("WM_DELETE_WINDOW",closeWindow)
root.mainloop()

