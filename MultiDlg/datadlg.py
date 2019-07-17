from PyQt5.QtWidgets import QDialog
#from PyQt5.QtCore import Qt
from ui_datadlg import Ui_DataDlg

class DataDlg(QDialog):
    def __init__(self, parent):
        super(DataDlg, self).__init__(parent)
        #self.setWindowFlags(Qt.Window)
        self.ui = Ui_DataDlg()
        self.ui.setupUi(self)

    def __del__(self):
        self.ui = None