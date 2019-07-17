# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ManualDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ManualDlg(object):
    def setupUi(self, ManualDlg):
        ManualDlg.setObjectName("ManualDlg")
        ManualDlg.resize(820, 520)
        ManualDlg.setStyleSheet("background-color: rgb(255, 170, 127);")

        self.retranslateUi(ManualDlg)
        QtCore.QMetaObject.connectSlotsByName(ManualDlg)

    def retranslateUi(self, ManualDlg):
        _translate = QtCore.QCoreApplication.translate
        ManualDlg.setWindowTitle(_translate("ManualDlg", "Manual"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManualDlg = QtWidgets.QDialog()
    ui = Ui_ManualDlg()
    ui.setupUi(ManualDlg)
    ManualDlg.show()
    sys.exit(app.exec_())

