from PyQt5.QtWidgets import QDialog
#from PyQt5.QtCore import Qt
from ui_manualdlg import Ui_ManualDlg

class ManualDlg(QDialog):
    def __init__(self, parent):
        super(ManualDlg, self).__init__(parent)
        #self.setWindowFlags(Qt.Window)
        self.ui = Ui_ManualDlg()
        self.ui.setupUi(self)

    def __del__(self):
        self.ui = None