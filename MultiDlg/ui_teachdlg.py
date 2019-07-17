# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TeachDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TeachDlg(object):
    def setupUi(self, TeachDlg):
        TeachDlg.setObjectName("TeachDlg")
        TeachDlg.resize(820, 520)
        TeachDlg.setStyleSheet("")
        self.widget = QtWidgets.QWidget(TeachDlg)
        self.widget.setGeometry(QtCore.QRect(10, 10, 481, 491))
        self.widget.setStyleSheet("QWidget{\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: black;\n"
"    padding: 3px;\n"
"}")
        self.widget.setObjectName("widget")
        self.tabWidget = QtWidgets.QTabWidget(TeachDlg)
        self.tabWidget.setGeometry(QtCore.QRect(500, 260, 301, 241))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.miniWidget = QtWidgets.QWidget(TeachDlg)
        self.miniWidget.setGeometry(QtCore.QRect(500, 10, 301, 241))
        self.miniWidget.setStyleSheet("QWidget{\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: black;\n"
"    padding: 3px;\n"
"}")
        self.miniWidget.setObjectName("miniWidget")

        self.retranslateUi(TeachDlg)
        QtCore.QMetaObject.connectSlotsByName(TeachDlg)

    def retranslateUi(self, TeachDlg):
        _translate = QtCore.QCoreApplication.translate
        TeachDlg.setWindowTitle(_translate("TeachDlg", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("TeachDlg", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("TeachDlg", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TeachDlg = QtWidgets.QWidget()
    ui = Ui_TeachDlg()
    ui.setupUi(TeachDlg)
    TeachDlg.show()
    sys.exit(app.exec_())

