from PyQt5.QtWidgets import QWidget,QApplication,QDialog
from UI_Convert.paramsCv_ui import Ui_paramsCv

class paramsCv(QDialog):
	def __init__(self,parent):
		super(paramsCv,self).__init__(parent)
		self.ui = Ui_paramsCv()
		self.ui.setupUi(self)
	
	def __del__(self):
		self.ui = None
