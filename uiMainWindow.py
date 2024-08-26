# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\python_demo\mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import os
import http_base
import threading
import time
from uiPic2Base64 import uiPic2Base64Dialog
import json

data_cmd = {
    "Type": 0,
    "Ch": 0,
    "Data": {}
}
json_dicts = {}

g_username = 'admin'
g_password = '1'
g_ipaddr = '10.8.0.38'
g_port = 80

cmd = ''

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.globalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.globalLayout.setSpacing(50)
        self.globalLayout.setContentsMargins(20, 20, 20, 20)

        self.deviceGridLayout = QtWidgets.QGridLayout()
        self.deviceGridLayout.setSpacing(20)
        self.deviceGridLayout.setContentsMargins(0, 0, 0, 0)

        self.ipAddrLabel = QtWidgets.QLabel()
        self.ipAddrLabel.setFixedWidth(100)
        self.ipAddrLabel.setText("IP")
        self.ipAddrLineEdit = QtWidgets.QLineEdit()
        self.ipAddrLineEdit.setFixedWidth(200)
        self.ipAddrLineEdit.setText(g_ipaddr)

        self.portLabel = QtWidgets.QLabel()
        self.portLabel.setFixedWidth(100)
        self.portLabel.setText("端口")
        self.portSpinBox = QtWidgets.QSpinBox()
        self.portSpinBox.setFixedWidth(100)
        self.portSpinBox.setValue(g_port)
        self.portSpinBox.setRange(1,65535)

        self.userNameLabel = QtWidgets.QLabel()
        self.userNameLabel.setFixedWidth(100)
        self.userNameLabel.setText("用户名")
        self.userNameLineEdit = QtWidgets.QLineEdit()
        self.userNameLineEdit.setFixedWidth(200)
        self.userNameLineEdit.setText(g_username)

        self.passwordLabel = QtWidgets.QLabel()
        self.passwordLabel.setFixedWidth(100)
        self.passwordLabel.setText("密码")
        self.passwordLineEdit = QtWidgets.QLineEdit()
        self.passwordLineEdit.setFixedWidth(200)
        self.passwordLineEdit.setText(g_password)

        self.deviceListCombo = QtWidgets.QComboBox()
        self.deviceListCombo.setFixedSize(300, 25)
        self.deviceListCombo.currentIndexChanged.connect(self.slotdeviceListComboChanged)
        self.deviceListRefreshBtn = QtWidgets.QPushButton()
        self.deviceListRefreshBtn.setText("刷新")
        self.deviceListRefreshBtn.clicked.connect(self.slotDeviceRefreshBtnClicked)

        self.picToBase64hBtn = QtWidgets.QPushButton()
        self.picToBase64hBtn.setText("图片转Base64")
        self.picToBase64hBtn.clicked.connect(self.slotPicToBase64BtnClicked)

        self.deviceGridLayout.addWidget(self.ipAddrLabel, 0, 0, 1, 1)
        self.deviceGridLayout.addWidget(self.ipAddrLineEdit, 0, 1, 1, 1)
        self.deviceGridLayout.addWidget(self.portLabel, 0, 2, 1, 1)
        self.deviceGridLayout.addWidget(self.portSpinBox, 0, 3, 1, 1)
        self.deviceGridLayout.addWidget(self.userNameLabel, 0, 4, 1, 1)
        self.deviceGridLayout.addWidget(self.userNameLineEdit, 0, 5, 1, 1)
        self.deviceGridLayout.addWidget(self.passwordLabel, 0, 6, 1, 1)
        self.deviceGridLayout.addWidget(self.passwordLineEdit, 0, 7, 1, 1)
        self.deviceGridLayout.addWidget(self.picToBase64hBtn, 0, 8, 1, 1)

        #下面的交互位置的代码
        self.contentLayout = QtWidgets.QHBoxLayout()
        self.contentLayout.setSpacing(20)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        #树控件
        self.cmdTreeWidget = QtWidgets.QTreeWidget()
        self.cmdTreeWidget.setFixedWidth(300)
        self.cmdTreeWidget.setColumnCount(1)
        self.cmdTreeWidget.clicked.connect(self.slotCmdTreeItemClicked)
        #两个文本框
        self.configAreaLayout = QtWidgets.QVBoxLayout()
        self.textAreaLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.sendUrlHLayout = QtWidgets.QHBoxLayout()
        self.sendUrlHLayout.setSpacing(20)
        self.sendUrlHLayout.setContentsMargins(0, 0, 0, 0)
        self.sendUrlLabel = QtWidgets.QLabel()
        self.sendUrlLabel.setText("URL")
        self.sendUrlLineEdit = QtWidgets.QLineEdit()
        self.sendUrlLineEdit.setReadOnly(True)
        self.sendUrlHLayout.addWidget(self.sendUrlLabel)
        self.sendUrlHLayout.addWidget(self.sendUrlLineEdit)

        self.sendAreaLayout = QtWidgets.QVBoxLayout()
        self.sendAreaLabel = QtWidgets.QLabel()
        self.sendAreaTextEdit = QtWidgets.QTextEdit()


        self.sendAreaLayout.addWidget(self.sendAreaLabel)
        self.sendAreaLayout.addWidget(self.sendAreaTextEdit)

        self.recieveAreaLayout = QtWidgets.QVBoxLayout()
        self.recieveAreaLabel = QtWidgets.QLabel()
        self.recieveAreaTextEdit = QtWidgets.QTextEdit()
        self.recieveAreaLayout.addWidget(self.recieveAreaLabel)
        self.recieveAreaLayout.addWidget(self.recieveAreaTextEdit)

        self.textAreaLayout.addLayout(self.sendAreaLayout)
        self.textAreaLayout.addLayout(self.recieveAreaLayout)

        self.sendJsonButton = QtWidgets.QPushButton()
        self.sendJsonButton.setMinimumWidth(100)
        self.sendJsonButton.setFixedHeight(30)
        self.sendJsonButton.clicked.connect(self.slotSendBtnClicked)
        #self.sendJsonButton.clicked.connect(self.slotSendTestBtnClicked)

        self.buttonLayout.addWidget(self.sendJsonButton, 0, QtCore.Qt.AlignCenter)

        self.configAreaLayout.addLayout(self.sendUrlHLayout)
        self.configAreaLayout.addLayout(self.textAreaLayout)
        self.configAreaLayout.addLayout(self.buttonLayout)

        self.contentLayout.addWidget(self.cmdTreeWidget)
        self.contentLayout.addLayout(self.configAreaLayout)

        self.globalLayout.addLayout(self.deviceGridLayout)
        self.globalLayout.addLayout(self.contentLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.initCommandTree()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sendAreaLabel.setText(_translate("MainWindow", "发送语义"))
        self.recieveAreaLabel.setText(_translate("MainWindow", "接收语义"))
        self.sendJsonButton.setText(_translate("MainWindow", "发送"))

    def setUiStyle(self):
        pass

    def initCommandTree(self):
        self.cmdTreeWidget.setColumnCount(1)
        self.cmdTreeWidget.setHeaderHidden(True)

        path = "./protocol"
        files = os.listdir(path)
        for file in files:
            with open(path + "/" + file, 'r', encoding='UTF-8') as fd:
                try:
                    arrayList = json.load(fd)
                except Exception as e:
                    self.sendAreaTextEdit.setTextColor(QtGui.QColor(255, 0, 0))
                    self.sendAreaTextEdit.append("文件：" + file)
                    self.sendAreaTextEdit.append("Json格式错误：\n" + str(e))
                    self.sendAreaTextEdit.append("\n")
                    continue;

                for jsonStr in arrayList['Array'] :
                    #print(jsonStr)
                    if not 'comment' in jsonStr:
                        desc = jsonStr['Desc']

                        #"""
                        if 'FirDesc' in desc:
                            found = 0
                            self.firRootItem = QtWidgets.QTreeWidgetItem()
                            self.firRootItem.setText(0, desc['FirDesc'])
                            rootCount = self.cmdTreeWidget.topLevelItemCount()
                            #print("rootcount = %d" % rootCount)
                            for i in range(0, rootCount):
                                rootItem = self.cmdTreeWidget.topLevelItem(i)
                                #print(rootItem.text(0))
                                if rootItem.text(0) == desc['FirDesc']:
                                    self.firRootItem = rootItem
                                    found = 1
                            if found == 0:
                                self.cmdTreeWidget.addTopLevelItem(self.firRootItem)

                            if 'SubDesc' in desc:
                                found = 0
                                self.subNode = QtWidgets.QTreeWidgetItem()
                                self.subNode.setText(0, desc['SubDesc'])
                                subCount = self.firRootItem.childCount()
                                #print("subCount = %d" % subCount)
                                for i in range(0, subCount):
                                    secNode = self.firRootItem.child(i)
                                    #print(secNode.text(0))
                                    if secNode.text(0) == desc['SubDesc']:
                                        self.subNode = secNode
                                        found = 1
                                if found == 0:
                                    self.firRootItem.addChild(self.subNode)

                                if 'ThiDesc' in desc:
                                    json_dicts[desc['ThiDesc']] = jsonStr
                                    found = 0
                                    self.thiNode = QtWidgets.QTreeWidgetItem()
                                    self.thiNode.setText(0, desc['ThiDesc'])
                                    thirCount = self.subNode.childCount()
                                    #print("thirCount = %d" % thirCount)
                                    for i in range(0, thirCount):
                                        thiNode = self.subNode.child(i)
                                        #print(thiNode.text(0))
                                        if thiNode.text(0) == desc['ThiDesc']:
                                            self.thiNode = thiNode
                                            found = 1
                                    if found == 0:
                                        self.subNode.addChild(self.thiNode)
                                else:
                                    json_dicts[desc['SubDesc']] = jsonStr
                            else:
                                json_dicts[desc['FirDesc']] = jsonStr

    def http_recv_timer(self):
        dirt = {'recv': ''}
        get_success = 0
        get_success = http_base.get_recv(dirt)
        if get_success:
            print('get success recv = %s' % dirt['recv'])
            self.recieveAreaTextEdit.clear()
            self.recieveAreaTextEdit.setText(json.dumps(json.loads(dirt['recv'], encoding='UTF-8'), ensure_ascii=False, sort_keys = False, indent = 2))


    def startRecvTask(self):
        self.recvTimer = QtCore.QTimer()
        self.recvTimer.timeout.connect(self.http_recv_timer)
        self.recvTimer.start(1000)

    def uidialog(self,text):
        self.errDialog = QtWidgets.QDialog()
        self.errDialog.setFixedSize(400, 200)
        self.errDialogGLayout = QtWidgets.QVBoxLayout(self.errDialog)
        self.errLabel = QtWidgets.QLabel()
        self.errLabel.setWordWrap(True)
        self.errLabel.setAlignment(Qt.AlignCenter)
        self.errLabel.setText(text)
        self.errDialogGLayout.addWidget(self.errLabel)
        self.errDialog.exec()

    def slotSendBtnClicked(self):
        print("send json button clicked.")
        ipaddr = self.ipAddrLineEdit.text()
        if len(ipaddr) == 0 :
            self.uidialog("请输入iP地址")
            return False
        port = self.portSpinBox.value()

        if port == 0 :
            self.uidialog("请输入合法端口")
            return False
        username = self.userNameLineEdit.text()
        if len(username) == 0:
            self.uidialog("请输入用户名")
            return False

        password = self.passwordLineEdit.text()

        text = self.sendAreaTextEdit.toPlainText()
        #Command = json_dicts[currentItem.text(0)]['cmd']
        #print(Command)
        try:
            cmd_data = json.loads(text)
        except Exception as e:
            self.errDialog = QtWidgets.QDialog()
            self.errDialog.setFixedSize(400, 200)
            self.errDialogGLayout = QtWidgets.QVBoxLayout(self.errDialog)
            self.errLabel = QtWidgets.QLabel()
            self.errLabel.setWordWrap(True)
            self.errLabel.setText(str(e))
            self.errDialogGLayout.addWidget(self.errLabel)
            self.errDialog.exec()
            return False

        self.recieveAreaTextEdit.clear()
        self.recieveAreaTextEdit.setText("等待接收数据...")
        print(json.dumps(cmd_data))
        success = http_base.send_http_request(username, password, ipaddr, port, cmd, json.dumps(cmd_data))
        if success == False :
            self.uidialog("发送失败")
            return False



    def slotSendTestBtnClicked(self):
        print("send json button clicked.11111")
        self.recieveAreaTextEdit.clear()
        self.recieveAreaTextEdit.setText("等待接收数据...")
        cmd_str = json.dumps(data_cmd)
        print(cmd_str)
        #http_base.send_http_request('admin','888888','10.8.0.198','80', 'frmUserLogin', cmd_str)
        #http_base.send_http_request('admin', '888888', '10.8.0.198', '80', 'frmUserLogout', cmd_str)
        #http_base.send_http_request('admin', '888888', '10.8.0.198', '80', 'frmDevicePara', cmd_str)
        http_base.send_http_request('admin', '888888', '10.8.0.198', '80', 'frmDeviceTimeCtrl', cmd_str)

    def slotDeviceRefreshBtnClicked(self):
        #user_list = http_base.get_online_device()
        user_list = ''
        print(user_list)
        self.deviceListCombo.clear()
        for user in user_list:
            self.deviceListCombo.addItem(user)

    def slotCmdTreeItemClicked(self):
        global currentItem
        currentItem = self.cmdTreeWidget.currentItem()
        #print("tree item clicked: %s" % currentItem.text(0))
        self.recieveAreaTextEdit.clear()
        global cmd
        if currentItem.text(0) in json_dicts:
            print(json_dicts[currentItem.text(0)])
            self.sendAreaTextEdit.setText(json.dumps(json_dicts[currentItem.text(0)]['Content'], sort_keys = False, indent = 2))
            ipaddr = self.ipAddrLineEdit.text()
            degisturi = 'http://'+ ipaddr +'//digest//' + json_dicts[currentItem.text(0)]['Command']
            cmd = json_dicts[currentItem.text(0)]['Command']
            self.sendUrlLineEdit.setText(degisturi)
        else:
            self.sendAreaTextEdit.clear()
            self.sendUrlLineEdit.clear()
            cmd = ''

    def slotdeviceListComboChanged(self):
        ip = self.deviceListCombo.currentText()
        #http_base.set_focus_device(ip)
        print("current ip: %s" % ip)

    def slotPicToBase64BtnClicked(self):
        self.uiPic2Base64Dialog = uiPic2Base64Dialog()
        self.uiPic2Base64Dialog.setupUi()
        self.uiPic2Base64Dialog.exec()