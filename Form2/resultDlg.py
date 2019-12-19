from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from header.resultUi import Ui_ResultDlg

class ResultDlg(QWidget):
    def __init__(self):
        super(ResultDlg,self).__init__()
        self.ui = Ui_ResultDlg()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)