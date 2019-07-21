# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cameraDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_camraDlg(object):
    def setupUi(self, camraDlg):
        camraDlg.setObjectName("camraDlg")
        camraDlg.resize(534, 393)
        self.label = QtWidgets.QLabel(camraDlg)
        self.label.setGeometry(QtCore.QRect(10, 10, 511, 311))
        self.label.setStyleSheet("QLabel\n"
" {\n"
"    background-color: black;\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: green;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}")
        self.label.setText("")
        self.label.setObjectName("label")
        self.but_start = QtWidgets.QPushButton(camraDlg)
        self.but_start.setGeometry(QtCore.QRect(20, 330, 80, 40))
        self.but_start.setStyleSheet("QPushButton {\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: green;\n"
"    font: bold 10px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0,255, 0);\n"
"    border-style: inset;\n"
"}")
        self.but_start.setObjectName("but_start")
        self.but_stop = QtWidgets.QPushButton(camraDlg)
        self.but_stop.setGeometry(QtCore.QRect(110, 330, 80, 40))
        self.but_stop.setStyleSheet("QPushButton {\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: green;\n"
"    font: bold 10px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(255,0, 0);\n"
"    border-style: inset;\n"
"}")
        self.but_stop.setObjectName("but_stop")
        self.ln_webcam = QtWidgets.QLineEdit(camraDlg)
        self.ln_webcam.setGeometry(QtCore.QRect(410, 330, 101, 20))
        self.ln_webcam.setObjectName("ln_webcam")
        self.ln_basler = QtWidgets.QLineEdit(camraDlg)
        self.ln_basler.setGeometry(QtCore.QRect(410, 360, 101, 20))
        self.ln_basler.setObjectName("ln_basler")
        self.rad_webcam = QtWidgets.QRadioButton(camraDlg)
        self.rad_webcam.setGeometry(QtCore.QRect(320, 330, 82, 20))
        self.rad_webcam.setObjectName("rad_webcam")
        self.rad_basler = QtWidgets.QRadioButton(camraDlg)
        self.rad_basler.setGeometry(QtCore.QRect(320, 360, 82, 20))
        self.rad_basler.setObjectName("rad_basler")
        self.but_capture = QtWidgets.QPushButton(camraDlg)
        self.but_capture.setGeometry(QtCore.QRect(200, 330, 80, 40))
        self.but_capture.setStyleSheet("QPushButton {\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: green;\n"
"    font: bold 10px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(255,0, 0);\n"
"    border-style: inset;\n"
"}")
        self.but_capture.setObjectName("but_capture")

        self.retranslateUi(camraDlg)
        QtCore.QMetaObject.connectSlotsByName(camraDlg)

    def retranslateUi(self, camraDlg):
        _translate = QtCore.QCoreApplication.translate
        camraDlg.setWindowTitle(_translate("camraDlg", "cameraDlg"))
        self.but_start.setText(_translate("camraDlg", "Start"))
        self.but_stop.setText(_translate("camraDlg", "Stop"))
        self.rad_webcam.setText(_translate("camraDlg", "webcam"))
        self.rad_basler.setText(_translate("camraDlg", "basler"))
        self.but_capture.setText(_translate("camraDlg", "Capture"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    camraDlg = QtWidgets.QWidget()
    ui = Ui_camraDlg()
    ui.setupUi(camraDlg)
    camraDlg.show()
    sys.exit(app.exec_())

