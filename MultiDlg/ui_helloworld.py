# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HelloWorld.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HelloWorldDlg(object):
    def setupUi(self, HelloWorldDlg):
        HelloWorldDlg.setObjectName("HelloWorldDlg")
        HelloWorldDlg.resize(800, 600)
        self.but_Auto = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_Auto.setGeometry(QtCore.QRect(15, 530, 65, 65))
        self.but_Auto.setStyleSheet("QPushButton{\n"
"    background-color: rgb(85, 170, 127);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(0, 170, 127);\n"
"}")
        self.but_Auto.setText("")
        self.but_Auto.setObjectName("but_Auto")
        self.mdiArea = QtWidgets.QMdiArea(HelloWorldDlg)
        self.mdiArea.setGeometry(QtCore.QRect(0, 0, 800, 520))
        self.mdiArea.setObjectName("mdiArea")
        self.but_Manual = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_Manual.setGeometry(QtCore.QRect(80, 530, 65, 65))
        self.but_Manual.setStyleSheet("QPushButton{\n"
"    background-color: rgb(85, 170, 127);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(0, 170, 127);\n"
"}")
        self.but_Manual.setText("")
        self.but_Manual.setObjectName("but_Manual")
        self.but_Teach = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_Teach.setGeometry(QtCore.QRect(145, 530, 65, 65))
        self.but_Teach.setStyleSheet("QPushButton{\n"
"    background-color: rgb(85, 170, 127);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(0, 170, 127);\n"
"}")
        self.but_Teach.setText("")
        self.but_Teach.setObjectName("but_Teach")
        self.but_Data = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_Data.setGeometry(QtCore.QRect(210, 530, 65, 65))
        self.but_Data.setStyleSheet("QPushButton{\n"
"    background-color: rgb(85, 170, 127);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(0, 170, 127);\n"
"}")
        self.but_Data.setText("")
        self.but_Data.setObjectName("but_Data")

        self.retranslateUi(HelloWorldDlg)
        QtCore.QMetaObject.connectSlotsByName(HelloWorldDlg)

    def retranslateUi(self, HelloWorldDlg):
        _translate = QtCore.QCoreApplication.translate
        HelloWorldDlg.setWindowTitle(_translate("HelloWorldDlg", "Automation Group"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HelloWorldDlg = QtWidgets.QDialog()
    ui = Ui_HelloWorldDlg()
    ui.setupUi(HelloWorldDlg)
    HelloWorldDlg.show()
    sys.exit(app.exec_())

