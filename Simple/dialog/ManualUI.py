# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'manual.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(876, 598)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 121, 191))
        self.groupBox.setObjectName("groupBox")
        self.but_onLed = QtWidgets.QPushButton(self.groupBox)
        self.but_onLed.setGeometry(QtCore.QRect(10, 40, 89, 25))
        self.but_onLed.setObjectName("but_onLed")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 210, 121, 381))
        self.groupBox_2.setObjectName("groupBox_2")
        self.lb_led = QtWidgets.QLabel(self.groupBox_2)
        self.lb_led.setGeometry(QtCore.QRect(20, 40, 81, 21))
        self.lb_led.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_led.setObjectName("lb_led")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(150, 10, 711, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.but_loadImage = QtWidgets.QPushButton(self.groupBox_3)
        self.but_loadImage.setGeometry(QtCore.QRect(10, 40, 89, 25))
        self.but_loadImage.setObjectName("but_loadImage")
        self.but_test = QtWidgets.QPushButton(self.groupBox_3)
        self.but_test.setGeometry(QtCore.QRect(110, 40, 89, 25))
        self.but_test.setObjectName("but_test")
        self.frame = QtWidgets.QLabel(Form)
        self.frame.setGeometry(QtCore.QRect(150, 100, 711, 491))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setObjectName("frame")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Input"))
        self.but_onLed.setText(_translate("Form", "On Led"))
        self.groupBox_2.setTitle(_translate("Form", "Output"))
        self.lb_led.setText(_translate("Form", "Led"))
        self.groupBox_3.setTitle(_translate("Form", "GroupBox"))
        self.but_loadImage.setText(_translate("Form", "Load Image"))
        self.but_test.setText(_translate("Form", "Test"))
        self.frame.setText(_translate("Form", "TextLabel"))

class ManualDlg(QtWidgets.QDialog):
    def __init__(self,parent):
        super(ManualDlg,self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def __del__(self):
        del self.ui


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
