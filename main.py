import wmi
from scapy.all import (
    ARP,
    Ether,
    getmacbyip,

)
import subprocess
from tkinter import Tk, Label
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyperclip
from PyQt5.QtWidgets import QMessageBox,QApplication
import ip
from mac import IP2MAC
import dname
from attack import *
import wol
import socket
addr = ip.find_local_ip()
args = "".join(addr)
ip_pre = '.'.join(args.split('.')[:-1])
ip.find_ip(ip_pre)
row_num = ip.live_ip

def build_packet(TargetIp, GateWayAddr):
        print("[-] Obtaining mac from {}".format(TargetIp))  # Print the message
        TargetMacAddr = None
        while not TargetMacAddr:
            TargetMacAddr = getmacbyip(TargetIp)  #Get MAC address
        MyMacAddr = get_if_hwaddr("WLAN")  #Get the MAC address of network card
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
            sendp(packet, inter=2, iface="WLAN")  #inter shows the duration of sending packet, iface show the internet speed
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
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  #Forbidden editing the table
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  #Column width adaption
        # self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        a = 0
        while a < row_num:
            self.tableWidget.setRowHeight(a, 10)  #row height
            a = a + 1

        arr = [[0] * 3 for _ in range(2000)]
        cc = 0
        ss = 0
        mac = []
        li = 0
        name1 = []
        aa = 0
#MAC address
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
#Device Name
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
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  #Centre Alignment
                self.tableWidget.setItem(i, j, newItem)

        #Allow right click action
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        #right click action
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.setLayout(layout)

    def generateMenu(self, pos):
        print(pos)
        #get the index the perform right click
        for i in self.tableWidget.selectionModel().selection().indexes():
            #get row index
            rowIndex = i.row()
            #if row index less than row number, display the menu
            if rowIndex < row_num:
                #create menu
                menu = QMenu()
                #create menu options
                item0 = menu.addAction("COPY NAME")
                item1 = menu.addAction("COPY IPV4 ADDRESS")
                item2 = menu.addAction("COPY MAC ADDRESS")
                item9 = menu.addAction("COPY ALL")
                item3 = menu.addAction("WOL")
                item4 = menu.addAction("PORT SCAN")
                item5 = menu.addAction("PING SCAN")
                item6 = menu.addAction("KICK")
                #Get the screen position
                screenPos = self.tableWidget.mapToGlobal(pos)
                #Action of menu
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
                    macAdd = self.tableWidget.item(rowIndex, 2).text()
                    if macAdd == "Unknown":
                        pass
                    else:
                        wol.wakeOn(deviceName, macAdd)
                elif action == item4:
                        ipdz = self.tableWidget.item(rowIndex, 1).text()
                        portop = []
                        a = 0
                        for port in range(0, 5000 + 1):
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.0000000001)
                            result = sock.connect_ex((ipdz, port))
                            if result == 0:
                                portop.append(port)
                                a = a + 1
                            else:
                                pass
                        root = Tk()
                        root.title("Port Result")
                        label = Label(root, text="It's have "+str(a)+" ports are opened"+"\n"+"It's have "+str(portop))
                        label.pack()
                        root.mainloop()
                elif action == item5:


                    def ping_host(host):
                        p = subprocess.Popen(["ping", "-n", "1", host], stdout=subprocess.PIPE)
                        output, _ = p.communicate()
                        return output

                    def show_ping_result():
                        host = self.tableWidget.item(rowIndex, 1).text()
                        output = ping_host(host)
                        root = Tk()
                        root.title("Ping Result")
                        label = Label(root, text=output)
                        label.pack()
                        root.mainloop()

                    show_ping_result()


                elif action == item6:
                    TargetIp = self.tableWidget.item(rowIndex, 1).text()  #The ip address of device
                    #Get wmi
                    wmi_obj = wmi.WMI()
                    wmi_sql = "select DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
                    wmi_out = wmi_obj.query(wmi_sql)
                    #Produce the packet
                    for dev in wmi_out:
                        gao = dev.DefaultIPGateway[0]
                    GateWayAddr = gao  #Get router address
                    signal.signal(signal.SIGINT, stop)
                    global packet
                    packet = build_packet(TargetIp, GateWayAddr)
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
        label.setText("The System is Running")
        label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.setGeometry(500, 500, 250, 250)
        self.setWindowTitle('Processing')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Error', "Is return to the origin interface?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            pass
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = TableWidgetContextMenu()
    main.show()
    sys.exit(app.exec_())

