# -*- coding: utf-8 -*-

import os,sys
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication,QWidget
from mainWindow import mainWindow

if __name__=='__main__': 
    #创建应用程序和对象
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())