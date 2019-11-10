# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auto.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(933, 599)
        self.clock = QtWidgets.QLabel(Form)
        self.clock.setGeometry(QtCore.QRect(10, 10, 281, 21))
        self.clock.setStyleSheet("font: 57 16pt \"Ubuntu\";")
        self.clock.setAlignment(QtCore.Qt.AlignCenter)
        self.clock.setObjectName("clock")

        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(90, 50, 201, 25))
        self.comboBox.setObjectName("comboBox")

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 70, 281, 141))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 67, 17))
        self.label_2.setObjectName("label_2")
        self.lb_ok = QtWidgets.QLabel(self.groupBox)
        self.lb_ok.setGeometry(QtCore.QRect(90, 40, 181, 21))
        self.lb_ok.setStyleSheet("font: 57 16pt \"Ubuntu\";")
        self.lb_ok.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_ok.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_ok.setObjectName("lb_ok")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 67, 17))
        self.label_4.setObjectName("label_4")
        self.lb_ng = QtWidgets.QLabel(self.groupBox)
        self.lb_ng.setGeometry(QtCore.QRect(90, 70, 181, 21))
        self.lb_ng.setStyleSheet("font: 57 16pt \"Ubuntu\";")
        self.lb_ng.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_ng.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_ng.setObjectName("lb_ng")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 100, 67, 17))
        self.label_6.setObjectName("label_6")
        self.lb_total = QtWidgets.QLabel(self.groupBox)
        self.lb_total.setGeometry(QtCore.QRect(90, 100, 181, 21))
        self.lb_total.setStyleSheet("font: 57 16pt \"Ubuntu\";")
        self.lb_total.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_total.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_total.setObjectName("lb_total")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 71, 21))
        self.label_3.setObjectName("label_3")

        self.lb_result = QtWidgets.QLabel(Form)
        self.lb_result.setGeometry(QtCore.QRect(10, 220, 281, 400))
        self.lb_result.setStyleSheet("font: 57 36pt \"Ubuntu\";")
        self.lb_result.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_result.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_result.setObjectName("lb_result")
        
        self.frame = QtWidgets.QLabel(Form)
        self.frame.setGeometry(QtCore.QRect(320, 50, 650, 570))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setText("")
        self.frame.setObjectName("frame")

        self.logProcess = QtWidgets.QListWidget(Form)
        self.logProcess.setGeometry(QtCore.QRect(1000, 50, 290, 570))
        self.logProcess.setObjectName("logProcess")
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.clock.setText(_translate("Form", "Clock"))
        self.label_2.setText(_translate("Form", "OK"))
        self.lb_ok.setText(_translate("Form", "0"))
        self.label_4.setText(_translate("Form", "NG"))
        self.lb_ng.setText(_translate("Form", "0"))
        self.label_6.setText(_translate("Form", "Total"))
        self.lb_total.setText(_translate("Form", "0"))
        self.label_3.setText(_translate("Form", "Model"))
        self.lb_result.setText(_translate("Form", "Result"))

class AutoDlg(QtWidgets.QDialog):
    def __init__(self,parent):
        super(AutoDlg,self).__init__(parent)
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
