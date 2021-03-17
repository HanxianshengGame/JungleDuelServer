#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/3/9 15:35
# @Author  : handling
# @File    : RPCClient.py
# @Software: PyCharm

from xmlrpclib import ServerProxy            #导入xmlrpclib的包
s = ServerProxy("http://localhost:8080") #定义xmlrpc客户端
print s.fun_add(2,3)



