from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from libs.labelDialog import LabelDialog

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myDlg = LabelDialog(listItem=["1","2"])
    myDlg.show()
    sys.exit(app.exec_())
