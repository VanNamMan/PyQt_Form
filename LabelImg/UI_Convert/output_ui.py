# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_output(object):
    def setupUi(self, output):
        output.setObjectName("output")
        output.resize(416, 389)
        self.tableWidget = QtWidgets.QTableWidget(output)
        self.tableWidget.setGeometry(QtCore.QRect(8, 20, 401, 211))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.retranslateUi(output)
        QtCore.QMetaObject.connectSlotsByName(output)

    def retranslateUi(self, output):
        _translate = QtCore.QCoreApplication.translate
        output.setWindowTitle(_translate("output", "output"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("output", "Output"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("output", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("output", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("output", "label"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("output", "value"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("output", "type"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("output", "descision"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    output = QtWidgets.QWidget()
    ui = Ui_output()
    ui.setupUi(output)
    output.show()
    sys.exit(app.exec_())

