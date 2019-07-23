from PyQt5.QtWidgets import QWidget,QApplication,QDialog
from UI_Convert.paramsCv_ui import Ui_paramsCv

class paramsCv(QDialog):
	def __init__(self,parent):
		super(paramsCv,self).__init__(parent)
		self.ui = Ui_paramsCv()
		self.ui.setupUi(self)
		self.ui.groupBox.setLayout(self.ui.verticalLayout)
		self.ui.groupBox_2.setLayout(self.ui.verticalLayout_2)
		self.ui.groupBox_3.setLayout(self.ui.verticalLayout_3)
		self.setLayout(self.ui.verticalLayout_5)
	def __del__(self):
		self.ui = None
