import gc
import sys
import ctypes


# 通过内存地址去访问没有引用的对象（unreachable objects）
class PyObject(ctypes.Structure):
    _fields_ = [("refcnt", ctypes.c_long)]

# 获取对象引用数量
print(PyObject.from_address(2891061213376).refcnt)