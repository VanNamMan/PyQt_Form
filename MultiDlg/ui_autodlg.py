# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AutoDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AutoDlg(object):
    def setupUi(self, AutoDlg):
        AutoDlg.setObjectName("AutoDlg")
        AutoDlg.resize(820, 520)
        AutoDlg.setStyleSheet("")
        self.lb_timer = QtWidgets.QLabel(AutoDlg)
        self.lb_timer.setGeometry(QtCore.QRect(700, 0, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lb_timer.setFont(font)
        self.lb_timer.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_timer.setObjectName("lb_timer")
        self.label = QtWidgets.QLabel(AutoDlg)
        self.label.setGeometry(QtCore.QRect(10, 40, 431, 441))
        self.label.setStyleSheet("QLabel{\n"
"    background-color: black;\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: white;\n"
"    padding: 6px;\n"
"}")
        self.label.setText("")
        self.label.setObjectName("label")
        self.groupBox_2 = QtWidgets.QGroupBox(AutoDlg)
        self.groupBox_2.setGeometry(QtCore.QRect(450, 230, 351, 251))
        self.groupBox_2.setStyleSheet("QGroupBox{\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color:  rgb(85, 170, 255);\n"
"    padding: 6px;\n"
"}")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.but_Reset = QtWidgets.QPushButton(self.groupBox_2)
        self.but_Reset.setGeometry(QtCore.QRect(210, 190, 100, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.but_Reset.setFont(font)
        self.but_Reset.setStyleSheet("QPushButton{\n"
"    background-color: rgb(255,170,0);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(255,255,0);\n"
"}")
        self.but_Reset.setObjectName("but_Reset")
        self.but_Stop = QtWidgets.QPushButton(self.groupBox_2)
        self.but_Stop.setGeometry(QtCore.QRect(110, 190, 100, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.but_Stop.setFont(font)
        self.but_Stop.setStyleSheet("QPushButton{\n"
"    background-color: rgb(170,0,0);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(255,0,0);\n"
"}")
        self.but_Stop.setObjectName("but_Stop")
        self.but_Start = QtWidgets.QPushButton(self.groupBox_2)
        self.but_Start.setGeometry(QtCore.QRect(10, 190, 100, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.but_Start.setFont(font)
        self.but_Start.setStyleSheet("QPushButton{\n"
"    background-color: rgb(0,170,0);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: rgb(0,255,0);\n"
"}\n"
"")
        self.but_Start.setObjectName("but_Start")
        self.listWidget = QtWidgets.QListWidget(self.groupBox_2)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 331, 171))
        self.listWidget.setStyleSheet("QListWidget{\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: italic 8px;\n"
"    padding: 6px;\n"
"}")
        self.listWidget.setObjectName("listWidget")
        self.groupBox = QtWidgets.QGroupBox(AutoDlg)
        self.groupBox.setGeometry(QtCore.QRect(450, 40, 351, 181))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("QGroupBox{\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color:  rgb(85, 170, 255);\n"
"    padding: 6px;\n"
"}")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 61, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setObjectName("label_2")
        self.lb_total = QtWidgets.QLabel(self.groupBox)
        self.lb_total.setGeometry(QtCore.QRect(90, 40, 47, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lb_total.setFont(font)
        self.lb_total.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lb_total.setObjectName("lb_total")
        self.lb_num_OK = QtWidgets.QLabel(self.groupBox)
        self.lb_num_OK.setGeometry(QtCore.QRect(90, 70, 47, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lb_num_OK.setFont(font)
        self.lb_num_OK.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lb_num_OK.setObjectName("lb_num_OK")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 47, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(0, 170, 0);")
        self.label_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_5.setObjectName("label_5")
        self.lb_num_NG = QtWidgets.QLabel(self.groupBox)
        self.lb_num_NG.setGeometry(QtCore.QRect(90, 100, 47, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lb_num_NG.setFont(font)
        self.lb_num_NG.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lb_num_NG.setObjectName("lb_num_NG")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 100, 47, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_7.setObjectName("label_7")
        self.lb_result_left = QtWidgets.QLabel(self.groupBox)
        self.lb_result_left.setGeometry(QtCore.QRect(160, 9, 171, 161))
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.lb_result_left.setFont(font)
        self.lb_result_left.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_result_left.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_result_left.setObjectName("lb_result_left")

        self.retranslateUi(AutoDlg)
        QtCore.QMetaObject.connectSlotsByName(AutoDlg)

    def retranslateUi(self, AutoDlg):
        _translate = QtCore.QCoreApplication.translate
        AutoDlg.setWindowTitle(_translate("AutoDlg", "Auto"))
        self.lb_timer.setText(_translate("AutoDlg", "Time"))
        self.but_Reset.setText(_translate("AutoDlg", "RESET"))
        self.but_Stop.setText(_translate("AutoDlg", "STOP"))
        self.but_Start.setText(_translate("AutoDlg", "START"))
        self.label_2.setText(_translate("AutoDlg", "Total"))
        self.lb_total.setText(_translate("AutoDlg", "0"))
        self.lb_num_OK.setText(_translate("AutoDlg", "0"))
        self.label_5.setText(_translate("AutoDlg", "OK"))
        self.lb_num_NG.setText(_translate("AutoDlg", "0"))
        self.label_7.setText(_translate("AutoDlg", "NG"))
        self.lb_result_left.setText(_translate("AutoDlg", "?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AutoDlg = QtWidgets.QDialog()
    ui = Ui_AutoDlg()
    ui.setupUi(AutoDlg)
    AutoDlg.show()
    sys.exit(app.exec_())

