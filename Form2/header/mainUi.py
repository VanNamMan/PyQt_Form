# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.actionsave_as = QtWidgets.QAction(MainWindow)
        self.actionsave_as.setObjectName("actionsave_as")
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.actionCamera = QtWidgets.QAction(MainWindow)
        self.actionCamera.setObjectName("actionCamera")
        self.actionvision_parameter = QtWidgets.QAction(MainWindow)
        self.actionvision_parameter.setObjectName("actionvision_parameter")
        self.actionversion = QtWidgets.QAction(MainWindow)
        self.actionversion.setObjectName("actionversion")
        self.actioninfomation = QtWidgets.QAction(MainWindow)
        self.actioninfomation.setObjectName("actioninfomation")
        self.menuFile.addAction(self.actionopen)
        self.menuFile.addAction(self.actionsave)
        self.menuFile.addAction(self.actionsave_as)
        self.menuFile.addAction(self.actionexit)
        self.menuAbout.addAction(self.actionversion)
        self.menuAbout.addAction(self.actioninfomation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionopen.setText(_translate("MainWindow", "open"))
        self.actionsave.setText(_translate("MainWindow", "save"))
        self.actionsave_as.setText(_translate("MainWindow", "save as..."))
        self.actionexit.setText(_translate("MainWindow", "exit"))
        self.actionCamera.setText(_translate("MainWindow", "camera"))
        self.actionvision_parameter.setText(_translate("MainWindow", "vision parameter"))
        self.actionversion.setText(_translate("MainWindow", "version"))
        self.actioninfomation.setText(_translate("MainWindow", "infomation"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
