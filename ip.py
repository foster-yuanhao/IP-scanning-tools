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
    Given the current IP address segment, then scan all addresses for the entire segment
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
    Get the current device IP address
    Return IP address
    """
    myname = socket.getfqdn(socket.gethostname())
    if myname.find(".") == -1:
        myaddr = socket.gethostbyname(myname)
        return myaddr
    else:
        a = myname.split(".")[0]
        myaddr = socket.gethostbyname(a)
        return myaddr

