from PyQt5 import QtCore, QtGui, QtWidgets

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 350)
        self.btn_readMusic = QtWidgets.QPushButton(Form)
        self.btn_readMusic.setGeometry(QtCore.QRect(140, 200, 93, 28))
        self.btn_readMusic.setObjectName("btn_readMusic")
        self.btn_play = QtWidgets.QPushButton(Form)
        self.btn_play.setGeometry(QtCore.QRect(310, 200, 93, 28))
        self.btn_play.setObjectName("btn_play")
        self.btn_pause = QtWidgets.QPushButton(Form)
        self.btn_pause.setGeometry(QtCore.QRect(490, 200, 93, 28))
        self.btn_pause.setObjectName("btn_pause")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 110, 81, 21))
        self.label.setObjectName("label")
        self.label_MusicMessage = QtWidgets.QLabel(Form)
        self.label_MusicMessage.setGeometry(QtCore.QRect(140, 110, 591, 21))
        self.label_MusicMessage.setObjectName("label_MusicMessage")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_readMusic.setText(_translate("Form", "读取音频"))
        self.btn_play.setText(_translate("Form", "播放"))
        self.btn_pause.setText(_translate("Form", "停止"))
        self.label.setText(_translate("Form", "当前播放:"))
        self.label_MusicMessage.setText(_translate("Form", "暂无"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

