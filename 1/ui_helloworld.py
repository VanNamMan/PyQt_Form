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
        HelloWorldDlg.resize(858, 581)
        HelloWorldDlg.setStyleSheet("")
        self.frame = QtWidgets.QLabel(HelloWorldDlg)
        self.frame.setGeometry(QtCore.QRect(10, 40, 551, 501))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setText("")
        self.frame.setObjectName("frame")
        self.listWidget = QtWidgets.QListWidget(HelloWorldDlg)
        self.listWidget.setGeometry(QtCore.QRect(570, 401, 281, 111))
        self.listWidget.setObjectName("listWidget")
        self.but_runTest = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_runTest.setGeometry(QtCore.QRect(750, 370, 50, 23))
        self.but_runTest.setObjectName("but_runTest")
        self.tableWidget = QtWidgets.QTableWidget(HelloWorldDlg)
        self.tableWidget.setGeometry(QtCore.QRect(570, 40, 121, 101))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.but_load = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_load.setGeometry(QtCore.QRect(620, 370, 50, 23))
        self.but_load.setObjectName("but_load")
        self.lb_xywh = QtWidgets.QLabel(HelloWorldDlg)
        self.lb_xywh.setGeometry(QtCore.QRect(10, 550, 141, 16))
        self.lb_xywh.setObjectName("lb_xywh")
        self.lb_color = QtWidgets.QLabel(HelloWorldDlg)
        self.lb_color.setGeometry(QtCore.QRect(380, 550, 181, 16))
        self.lb_color.setObjectName("lb_color")
        self.lb_xy = QtWidgets.QLabel(HelloWorldDlg)
        self.lb_xy.setGeometry(QtCore.QRect(170, 550, 141, 16))
        self.lb_xy.setObjectName("lb_xy")
        self.but_save = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_save.setGeometry(QtCore.QRect(800, 370, 50, 23))
        self.but_save.setObjectName("but_save")
        self.but_start = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_start.setGeometry(QtCore.QRect(570, 520, 70, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.but_start.setFont(font)
        self.but_start.setObjectName("but_start")
        self.but_reset = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_reset.setGeometry(QtCore.QRect(640, 520, 70, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.but_reset.setFont(font)
        self.but_reset.setObjectName("but_reset")
        self.but_stop = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_stop.setGeometry(QtCore.QRect(710, 520, 70, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.but_stop.setFont(font)
        self.but_stop.setObjectName("but_stop")
        self.tabWidget = QtWidgets.QTabWidget(HelloWorldDlg)
        self.tabWidget.setGeometry(QtCore.QRect(570, 140, 281, 221))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 270, 200))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.ln_area = QtWidgets.QLineEdit(self.groupBox)
        self.ln_area.setGeometry(QtCore.QRect(50, 130, 30, 15))
        self.ln_area.setObjectName("ln_area")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 47, 15))
        self.label_5.setObjectName("label_5")
        self.ln_height = QtWidgets.QLineEdit(self.groupBox)
        self.ln_height.setGeometry(QtCore.QRect(50, 110, 30, 15))
        self.ln_height.setObjectName("ln_height")
        self.ln_width = QtWidgets.QLineEdit(self.groupBox)
        self.ln_width.setGeometry(QtCore.QRect(50, 90, 30, 15))
        self.ln_width.setObjectName("ln_width")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 47, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 47, 15))
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 60, 47, 15))
        self.label.setObjectName("label")
        self.sl_kthresh = QtWidgets.QSlider(self.groupBox)
        self.sl_kthresh.setGeometry(QtCore.QRect(50, 60, 161, 20))
        self.sl_kthresh.setMaximum(255)
        self.sl_kthresh.setOrientation(QtCore.Qt.Horizontal)
        self.sl_kthresh.setObjectName("sl_kthresh")
        self.lb_kthresh = QtWidgets.QLabel(self.groupBox)
        self.lb_kthresh.setGeometry(QtCore.QRect(170, 40, 41, 20))
        self.lb_kthresh.setObjectName("lb_kthresh")
        self.lb_name = QtWidgets.QLabel(self.groupBox)
        self.lb_name.setGeometry(QtCore.QRect(10, 20, 47, 15))
        self.lb_name.setObjectName("lb_name")
        self.ln_rect = QtWidgets.QLineEdit(self.groupBox)
        self.ln_rect.setGeometry(QtCore.QRect(50, 160, 81, 16))
        self.ln_rect.setObjectName("ln_rect")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 160, 31, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(90, 90, 47, 15))
        self.label_7.setObjectName("label_7")
        self.ln_padding = QtWidgets.QLineEdit(self.groupBox)
        self.ln_padding.setGeometry(QtCore.QRect(140, 90, 30, 15))
        self.ln_padding.setObjectName("ln_padding")
        self.ln_ratio = QtWidgets.QLineEdit(self.groupBox)
        self.ln_ratio.setGeometry(QtCore.QRect(140, 110, 30, 15))
        self.ln_ratio.setObjectName("ln_ratio")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(90, 110, 47, 15))
        self.label_8.setObjectName("label_8")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.list_funcs = QtWidgets.QListWidget(HelloWorldDlg)
        self.list_funcs.setGeometry(QtCore.QRect(700, 40, 151, 101))
        self.list_funcs.setObjectName("list_funcs")
        self.but_live = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_live.setGeometry(QtCore.QRect(570, 370, 50, 23))
        self.but_live.setObjectName("but_live")
        self.but_log = QtWidgets.QPushButton(HelloWorldDlg)
        self.but_log.setGeometry(QtCore.QRect(780, 520, 70, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.but_log.setFont(font)
        self.but_log.setObjectName("but_log")

        self.retranslateUi(HelloWorldDlg)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HelloWorldDlg)

    def retranslateUi(self, HelloWorldDlg):
        _translate = QtCore.QCoreApplication.translate
        HelloWorldDlg.setWindowTitle(_translate("HelloWorldDlg", "HelloWorld"))
        self.but_runTest.setText(_translate("HelloWorldDlg", "Run-Test"))
        self.but_load.setText(_translate("HelloWorldDlg", "Load Img"))
        self.lb_xywh.setText(_translate("HelloWorldDlg", "x,y,w,h"))
        self.lb_color.setText(_translate("HelloWorldDlg", "color"))
        self.lb_xy.setText(_translate("HelloWorldDlg", "x,y"))
        self.but_save.setText(_translate("HelloWorldDlg", "Save"))
        self.but_start.setText(_translate("HelloWorldDlg", "Start"))
        self.but_reset.setText(_translate("HelloWorldDlg", "Stop"))
        self.but_stop.setText(_translate("HelloWorldDlg", "Reset"))
        self.ln_area.setText(_translate("HelloWorldDlg", "-1,-1"))
        self.label_5.setText(_translate("HelloWorldDlg", "area"))
        self.ln_height.setText(_translate("HelloWorldDlg", "-1,-1"))
        self.ln_width.setText(_translate("HelloWorldDlg", "-1,-1"))
        self.label_3.setText(_translate("HelloWorldDlg", "width"))
        self.label_4.setText(_translate("HelloWorldDlg", "height"))
        self.label.setText(_translate("HelloWorldDlg", "kthresh"))
        self.lb_kthresh.setText(_translate("HelloWorldDlg", "0"))
        self.lb_name.setText(_translate("HelloWorldDlg", "name"))
        self.ln_rect.setText(_translate("HelloWorldDlg", "0,0,0,0"))
        self.label_6.setText(_translate("HelloWorldDlg", "rect"))
        self.label_7.setText(_translate("HelloWorldDlg", "padding"))
        self.ln_padding.setText(_translate("HelloWorldDlg", "5"))
        self.ln_ratio.setText(_translate("HelloWorldDlg", "0.5,1.5"))
        self.label_8.setText(_translate("HelloWorldDlg", "threshold"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("HelloWorldDlg", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("HelloWorldDlg", "Tab 2"))
        self.but_live.setText(_translate("HelloWorldDlg", "Live"))
        self.but_log.setText(_translate("HelloWorldDlg", "Log"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HelloWorldDlg = QtWidgets.QDialog()
    ui = Ui_HelloWorldDlg()
    ui.setupUi(HelloWorldDlg)
    HelloWorldDlg.show()
    sys.exit(app.exec_())

