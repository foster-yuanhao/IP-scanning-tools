# -*- coding: utf-8 -*-

import platform
import os
import threading
import socket
ipaddress = []
live_ip = 0
def get_os():
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
    for line in output:
        if str(line).upper().find("TTL") >= 0:
            global ipaddress
            ipaddress.append(ip_str)
            global live_ip
            live_ip += 1
            break


def find_ip(ip_prefix):
    '''''
    给出当前的ip地址段 ，然后扫描整个段所有地址
    '''
    threads = []
    for i in range(1, 256):
        ip = '%s.%s' % (ip_prefix, i)
        threads.append(threading.Thread(target=ping_ip, args={ip, }))
    for i in threads:
        i.start()
    for i in threads:
        i.join()


def find_local_ip():
    """
    获取本机当前ip地址
    :return: 返回本机ip地址
    """

    myname = socket.getfqdn(socket.gethostname())
    if myname.find(".") == -1:
        myaddr = socket.gethostbyname(myname)
        return myaddr
    else:
        a = myname.split(".")[0]#0表示留下的部分 0是前面 1是后面
        myaddr = socket.gethostbyname(a)
        return myaddr

