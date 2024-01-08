import pickle

"""
序列化过程将文本信息转变为二进制数据流。
这样就信息就容易存储在硬盘之中，当需要读取文件的时候，从硬盘中读取数据，然后再将其反序列化便可以得到原始的数据
1.便于存储
2.便于传输

pickle模块是以二进制的形式序列化后保存到文件中（保存文件的后缀为”.pkl”），不能直接打开进行预览。
而python的另一个序列化标准模块json，则是human-readable的，可以直接打开查看（例如在notepad++中查看

在pickle中dumps()和loads()操作的是bytes类型，而在使用dump()和load()读写文件时，要使用rb或wb模式，也就是只接收bytes类型的数据。
1. pickle.dump(obj, file)
将Python数据转换并保存到pickle格式的文件内。
关于参数file，有一点需要注意，必须是以二进制的形式进行操作（写入
    with open('data.pickle', 'wb') as f: 
        pickle.dump(data, f)
2. pickle.dumps(obj)
将Python数据转换为pickle格式的bytes字串。
    import pickle
    dic = {"k1":"v1","k2":123}
    s = pickle.dumps(dic)
    print(s)

pickle.dumps()方法跟pickle.dump()方法的区别在于，pickle.dumps()方法不需要写入文件中，它是直接返回一个序列化的bytes对象

3. pickle.load(file)
从pickle格式的文件中读取数据并转换为Python的类型。
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)

4. pickle.loads(bytes_object)
将pickle格式的bytes字串转换为Python的类型。
    import pickle
    dic = {"k1":"v1","k2":123}
    s = pickle.dumps(dic)
    dic2 = pickle.loads(s)
    print(dic2)

pickle.loads()方法跟pickle.load()方法的区别在于，pickle.loads()方法是直接从bytes对象中读取序列化的信息，而非从文件中读取。
"""


def local_pickle_001():
    """
    :return:
    """
    dic = {"k1": "v1", "k2": 123}
    s = pickle.dumps(dic)
    print(s)  # b'\x80\x03}q\x00(X\x02\x00\x00\x00k1q\x01X\x02\x00\x00\x00v1q\x02X\x02\x00\x00\x00k2q\x03K{u.'
    print(type(s))  # <class 'bytes'>
    # print(s.decode("gbk"))
    print(str(s))  # b'\x80\x03}q\x00(X\x02\x00\x00\x00k1q\x01X\x02\x00\x00\x00v1q\x02X\x02\x00\x00\x00k2q\x03K{u.'
    print(pickle.loads(s))  # {'k1': 'v1', 'k2': 123}
    print(type(pickle.loads(s)))  # <class 'dict'>


def local_pickle_002():
    """
    验证pickle模块的保存形式
    :return:
    """
    dic = {"k1": "v1", "k2": 123}
    with open(r".\temp\pickle_temp_01.pickle", "wb") as fw:
        pickle.dump(dic, fw)
    # 这里报错TypeError: a bytes-like object is required, not 'str'
    with open(r".\temp\json_temp_01.txt", "wb") as fw:
        import json
        json.dump(dic, fw)
    # with open(r".\temp\json_temp_01.txt", "w") as fw:
    #     import json
    #     json.dump(dic, fw)
    # with open(r".\temp\json_temp_01.json", "w") as fw:
    #     import json
    #     json.dump(dic, fw)


if __name__ == '__main__':
    pass
    local_pickle_001()
    # local_pickle_002()

