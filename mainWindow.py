# -*- coding: utf-8 -*-

import os,sys
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication,QWidget 
from uiMainWindow import Ui_MainWindow
import socket
import http_base

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startRecvTask()

       # http_base.http_base_init()

    		
        """
        self.ui.textEditRecieveJson.setReadOnly(True)
        self.ui.sendButton.clicked.connect(self.sendButtonClicked)
        # 给button 的 点击动作绑定一个事件处理函数
        """
            
    """def sendButtonClicked(self):
        self.ui.textEditRecieveJson.setText(self.ui.textEditSendJson.toPlainText())
    """
