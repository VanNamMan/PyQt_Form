# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/treeShape.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TreeShape(object):
    def setupUi(self, TreeShape):
        TreeShape.setObjectName("TreeShape")
        TreeShape.resize(400, 588)
        self.verticalLayoutWidget = QtWidgets.QWidget(TreeShape)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(190, 50, 160, 441))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.listShape = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listShape.setObjectName("listShape")
        self.verticalLayout.addWidget(self.listShape)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)

        self.retranslateUi(TreeShape)
        QtCore.QMetaObject.connectSlotsByName(TreeShape)

    def retranslateUi(self, TreeShape):
        _translate = QtCore.QCoreApplication.translate
        TreeShape.setWindowTitle(_translate("TreeShape", "Form"))
        self.label_2.setText(_translate("TreeShape", "Shape"))
        self.label.setText(_translate("TreeShape", "Function"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TreeShape = QtWidgets.QWidget()
    ui = Ui_TreeShape()
    ui.setupUi(TreeShape)
    TreeShape.show()
    sys.exit(app.exec_())
