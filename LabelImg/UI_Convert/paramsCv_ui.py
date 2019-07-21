# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paramsCv.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_paramsCv(object):
    def setupUi(self, paramsCv):
        paramsCv.setObjectName("paramsCv")
        paramsCv.resize(220, 523)
        self.groupBox = QtWidgets.QGroupBox(paramsCv)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 181, 151))
        self.groupBox.setStyleSheet("QGroupBox{\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color:  rgb(85, 170, 127);\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 47, 20))
        self.label.setObjectName("label")
        self.ln_kThresh = QtWidgets.QLineEdit(self.groupBox)
        self.ln_kThresh.setGeometry(QtCore.QRect(80, 30, 71, 20))
        self.ln_kThresh.setObjectName("ln_kThresh")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 47, 20))
        self.label_2.setObjectName("label_2")
        self.ln_blockSize = QtWidgets.QLineEdit(self.groupBox)
        self.ln_blockSize.setGeometry(QtCore.QRect(80, 60, 71, 20))
        self.ln_blockSize.setObjectName("ln_blockSize")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 47, 20))
        self.label_3.setObjectName("label_3")
        self.ln_C = QtWidgets.QLineEdit(self.groupBox)
        self.ln_C.setGeometry(QtCore.QRect(80, 90, 71, 20))
        self.ln_C.setObjectName("ln_C")
        self.ch_useOtsu = QtWidgets.QCheckBox(self.groupBox)
        self.ch_useOtsu.setGeometry(QtCore.QRect(20, 120, 70, 20))
        self.ch_useOtsu.setObjectName("ch_useOtsu")
        self.ch_normal = QtWidgets.QCheckBox(self.groupBox)
        self.ch_normal.setGeometry(QtCore.QRect(90, 120, 70, 20))
        self.ch_normal.setObjectName("ch_normal")
        self.groupBox_2 = QtWidgets.QGroupBox(paramsCv)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 180, 181, 151))
        self.groupBox_2.setStyleSheet("QGroupBox{\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color:  rgb(85, 170, 127);\n"
"\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}")
        self.groupBox_2.setObjectName("groupBox_2")
        self.ln_iter = QtWidgets.QLineEdit(self.groupBox_2)
        self.ln_iter.setGeometry(QtCore.QRect(80, 80, 71, 20))
        self.ln_iter.setObjectName("ln_iter")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(20, 80, 47, 20))
        self.label_9.setObjectName("label_9")
        self.ln_kSize = QtWidgets.QLineEdit(self.groupBox_2)
        self.ln_kSize.setGeometry(QtCore.QRect(80, 50, 71, 20))
        self.ln_kSize.setObjectName("ln_kSize")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(20, 50, 47, 20))
        self.label_8.setObjectName("label_8")
        self.groupBox_3 = QtWidgets.QGroupBox(paramsCv)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 350, 181, 151))
        self.groupBox_3.setStyleSheet("QGroupBox{\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color:  rgb(85, 170, 127);\n"
"\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}")
        self.groupBox_3.setObjectName("groupBox_3")
        self.ln_height = QtWidgets.QLineEdit(self.groupBox_3)
        self.ln_height.setGeometry(QtCore.QRect(80, 60, 71, 20))
        self.ln_height.setObjectName("ln_height")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(20, 30, 61, 20))
        self.label_7.setObjectName("label_7")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(20, 60, 47, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(20, 90, 47, 20))
        self.label_11.setObjectName("label_11")
        self.ln_width = QtWidgets.QLineEdit(self.groupBox_3)
        self.ln_width.setGeometry(QtCore.QRect(80, 30, 71, 20))
        self.ln_width.setObjectName("ln_width")
        self.ln_area = QtWidgets.QLineEdit(self.groupBox_3)
        self.ln_area.setGeometry(QtCore.QRect(80, 90, 71, 20))
        self.ln_area.setObjectName("ln_area")

        self.retranslateUi(paramsCv)
        QtCore.QMetaObject.connectSlotsByName(paramsCv)

    def retranslateUi(self, paramsCv):
        _translate = QtCore.QCoreApplication.translate
        paramsCv.setWindowTitle(_translate("paramsCv", "Parameter Vission"))
        self.groupBox.setTitle(_translate("paramsCv", "threshold"))
        self.label.setText(_translate("paramsCv", "k-thresh"))
        self.label_2.setText(_translate("paramsCv", "blockSize"))
        self.label_3.setText(_translate("paramsCv", "C"))
        self.ch_useOtsu.setText(_translate("paramsCv", "useOtsu"))
        self.ch_normal.setText(_translate("paramsCv", "normal"))
        self.groupBox_2.setTitle(_translate("paramsCv", "morphology"))
        self.label_9.setText(_translate("paramsCv", "iter"))
        self.label_8.setText(_translate("paramsCv", "k-size"))
        self.groupBox_3.setTitle(_translate("paramsCv", "removeBlobs"))
        self.label_7.setText(_translate("paramsCv", "width"))
        self.label_10.setText(_translate("paramsCv", "height"))
        self.label_11.setText(_translate("paramsCv", "area"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    paramsCv = QtWidgets.QWidget()
    ui = Ui_paramsCv()
    ui.setupUi(paramsCv)
    paramsCv.show()
    sys.exit(app.exec_())

