# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import base64

class uiPic2Base64Dialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.resize(900, 500)
        self.setWindowTitle('Image to Base64 code')

    def setupUi(self):
        self.globalLayout = QtWidgets.QHBoxLayout(self)

        self.leftWidget = QtWidgets.QWidget()
        self.leftVLayout = QtWidgets.QVBoxLayout(self.leftWidget)

        self.picLabel = QtWidgets.QLabel()
        self.picLabel.setScaledContents(True)
        self.picLabel.setFrameShape(QtWidgets.QFrame.Box)
        elf.picLabel.setText("No picture")
        self.picLabel.setFixedSize(400, 500)

        self.leftBottomWidget = QtWidgets.QWidget()
        self.leftBottomHLayout = QtWidgets.QHBoxLayout(self.leftBottomWidget)

        self.openPicBtn = QtWidgets.QPushButton()
        self.openPicBtn.setText("Open picture")
        self.openPicBtn.clicked.connect(self.slotOpenPicBtnClicked)
        self.savePicBtn = QtWidgets.QPushButton()
        self.savePicBtn.setText("Save picture")
        self.savePicBtn.clicked.connect(self.slotSavePicBtnClicked)

        self.leftBottomHLayout.addWidget(self.openPicBtn)
        self.leftBottomHLayout.addWidget(self.savePicBtn)

        self.leftVLayout.addWidget(self.picLabel)
        self.leftVLayout.addWidget(self.leftBottomWidget)

        self.centerWidget = QtWidgets.QWidget()
        self.centerVLayout = QtWidgets.QVBoxLayout(self.centerWidget)

        self.pic2Base64Btn = QtWidgets.QPushButton()
        self.pic2Base64Btn.setText("=>")
        self.pic2Base64Btn.setFixedSize(50, 30)
        self.pic2Base64Btn.clicked.connect(self.slotPic2Base64BtnClicked)
        self.base64code2PicBtn = QtWidgets.QPushButton()
        self.base64code2PicBtn.setText("<=")
        self.base64code2PicBtn.setFixedSize(50, 30)
        self.base64code2PicBtn.clicked.connect(self.slotBase64code2PicBtnClicked)

        self.centerVLayout.addWidget(self.pic2Base64Btn)
        self.centerVLayout.addWidget(self.base64code2PicBtn)

        self.rightWidget = QtWidgets.QWidget()
        self.rightVLayout = QtWidgets.QVBoxLayout(self.rightWidget)

        self.base64TextEdit = QtWidgets.QTextEdit()
        self.base64TextEdit.setFixedSize(400, 500)

        self.rightBottomWidget = QtWidgets.QWidget()
        self.rightBottomHLayout = QtWidgets.QHBoxLayout(self.rightBottomWidget)

        self.clearTextBtn = QtWidgets.QPushButton()
        self.clearTextBtn.setText("clear")
        self.clearTextBtn.clicked.connect(self.slotClearTextBtnClicked)

        self.rightBottomHLayout.addWidget(self.clearTextBtn)

        self.rightVLayout.addWidget(self.base64TextEdit)
        self.rightVLayout.addWidget(self.rightBottomWidget)

        self.globalLayout.addWidget(self.leftWidget)
        self.globalLayout.addWidget(self.centerWidget)
        self.globalLayout.addWidget(self.rightWidget)

    def slotPic2Base64BtnClicked(self):
        pixmap = self.picLabel.pixmap()
        if pixmap == None:
            print("No picture")
            return False

        tmp_path = './tmp_pic.jpg'
        pixmap.save(tmp_path)
        self.base64TextEdit.clear()
        with open(tmp_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            self.base64TextEdit.setText(base64_data.decode())
        QtCore.QFile.remove(tmp_path)

    def slotBase64code2PicBtnClicked(self):
        if len(self.base64TextEdit.toPlainText()) == 0:
            return False
        self.picLabel.clear()
        text = self.base64TextEdit.toPlainText()
        try:
            image_data = base64.b64decode(text)
        except:
            return False

        tmp_path = "./modal.jpg"
        with open(tmp_path, "wb") as f:
            f.write(image_data)
        self.picLabel.setPixmap(QtGui.QPixmap(tmp_path))
        QtCore.QFile.remove(tmp_path)


    def slotOpenPicBtnClicked(self):
        picName = QtWidgets.QFileDialog.getOpenFileName(filter = '*.jpg')[0]
        if (len(picName) > 0):
            self.picLabel.setPixmap(QtGui.QPixmap(picName))

    def slotSavePicBtnClicked(self):
        if self.picLabel.pixmap():
            savePath = QtWidgets.QFileDialog.getSaveFileName(filter = '*.jpg')[0]
            self.picLabel.pixmap().save(savePath)

    def slotClearTextBtnClicked(self):
        self.base64TextEdit.clear()

