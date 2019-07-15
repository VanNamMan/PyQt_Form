# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myForm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_myForm(object):
    def setupUi(self, myForm):
        myForm.setObjectName("myForm")
        myForm.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(myForm)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 521, 541))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.miniWidget = QtWidgets.QWidget(self.centralwidget)
        self.miniWidget.setGeometry(QtCore.QRect(540, 10, 251, 211))
        self.miniWidget.setStyleSheet("")
        self.miniWidget.setObjectName("miniWidget")
        myForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(myForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        myForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(myForm)
        self.statusbar.setObjectName("statusbar")
        myForm.setStatusBar(self.statusbar)

        self.retranslateUi(myForm)
        QtCore.QMetaObject.connectSlotsByName(myForm)

    def retranslateUi(self, myForm):
        _translate = QtCore.QCoreApplication.translate
        myForm.setWindowTitle(_translate("myForm", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myForm = QtWidgets.QMainWindow()
    ui = Ui_myForm()
    ui.setupUi(myForm)
    myForm.show()
    sys.exit(app.exec_())

