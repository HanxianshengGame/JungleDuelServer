#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/3/9 15:31
# @Author  : handling
# @File    : RPCServer.py
# @Software: PyCharm


from SimpleXMLRPCServer import SimpleXMLRPCServer


def fun_add(a, b):
    totle = a + b
    return totle


if __name__ == '__main__':
    s = SimpleXMLRPCServer(('0.0.0.0', 8080))  # 开启xmlrpcserver
    s.register_function(fun_add)  # 注册函数fun_add
    print "server is online..."
    s.serve_forever()  # 开启循环等待
