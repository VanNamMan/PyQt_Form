# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frame.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 300)
        self.frame = QtWidgets.QLabel(Frame)
        self.frame.setGeometry(QtCore.QRect(10, 10, 381, 251))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setText("")
        self.frame.setObjectName("frame")
        self.but_live = QtWidgets.QPushButton(Frame)
        self.but_live.setGeometry(QtCore.QRect(20, 270, 75, 23))
        self.but_live.setObjectName("but_live")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.but_live.setText(_translate("Frame", "Live"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QWidget()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

