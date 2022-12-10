import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyperclip
import ip
from mac import IP2MAC
import dname

addr = ip.find_local_ip()
args = "".join(addr)
ip_pre = '.'.join(args.split('.')[:-1])
ip.find_ip(ip_pre)
row_num = ip.live_ip

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
 # MAC部分
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
 #IP部分
        for cc in range(row_num):
            arr[cc][1] = ip.ipaddress[cc]
            cc = cc + 1
 #名称部分
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
                item1 = menu.addAction("COPY IPV4 ADDRESS")
                item2 = menu.addAction("COPY MAC ADDRESS")
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
                elif action == item2:
                    pyperclip.copy(self.tableWidget.item(rowIndex, 2).text())
                elif action == item3:
                    print("a")
                elif action == item4:
                    print("a")
                elif action == item5:
                    print("a")
                elif action == item6:
                    print("a")
            else:
                return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = TableWidgetContextMenu()
    main.show()
    sys.exit(app.exec_())
