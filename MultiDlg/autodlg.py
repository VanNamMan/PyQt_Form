from PyQt5.QtWidgets import QDialog
#from PyQt5.QtCore import Qt
from ui_autodlg import Ui_AutoDlg

class AutoDlg(QDialog):
    def __init__(self, parent):
        super(AutoDlg, self).__init__(parent)
        #self.setWindowFlags(Qt.Window)
        self.ui = Ui_AutoDlg()
        self.ui.setupUi(self)

    def __del__(self):
        self.ui = None