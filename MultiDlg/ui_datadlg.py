# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DataDlg(object):
    def setupUi(self, DataDlg):
        DataDlg.setObjectName("DataDlg")
        DataDlg.resize(820, 520)
        DataDlg.setStyleSheet("")

        self.retranslateUi(DataDlg)
        QtCore.QMetaObject.connectSlotsByName(DataDlg)

    def retranslateUi(self, DataDlg):
        _translate = QtCore.QCoreApplication.translate
        DataDlg.setWindowTitle(_translate("DataDlg", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DataDlg = QtWidgets.QWidget()
    ui = Ui_DataDlg()
    ui.setupUi(DataDlg)
    DataDlg.show()
    sys.exit(app.exec_())

