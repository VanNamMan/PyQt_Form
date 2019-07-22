from PyQt5.QtWidgets import QWidget,QApplication,QDialog,QComboBox
from UI_Convert.output_ui import Ui_output

class ouput(QDialog):
	def __init__(self,parent):
		super(ouput,self).__init__(parent)
		self.ui = Ui_output()
		self.ui.setupUi(self)

		self.cbbDescision = QComboBox(self)
		for item in ["Compare","Value"]:
			self.cbbDescision.addItem(item)
		self.ui.tableWidget.setCellWidget(1,4,self.cbbDescision)
	
	def __del__(self):
		self.ui = None
