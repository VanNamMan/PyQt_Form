from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from libs.utils import *
from libs.files import *

from configparser import ConfigParser



class setting(QDialog):
	def __init__(self,parent):
		super(setting,self).__init__(parent)
		self.setWindowTitle("Settings")
		self.setGeometry(QRect(200,100,200,500))

		layout = QVBoxLayout()

		group_binary = newWidget(self,QGroupBox,"Binary")
		group_removeContours = newWidget(self,QGroupBox,"Remove Contours")
		group_blurAndMorph = newWidget(self,QGroupBox,"Blur , Morphology")

		lb_thresh = newWidget(self,QLabel,"k-thresh")
		self.edit_thresh = newWidget(self,QLineEdit,"150")

		lb_c = newWidget(self,QLabel,"C")
		self.edit_c = newWidget(self,QLineEdit,"3")

		lb_blockSize = newWidget(self,QLabel,"blockSize")
		self.edit_blockSize = newWidget(self,QLineEdit,"11")

		lb_rangeWidth = newWidget(self,QLabel,"rangeWidth")
		self.edit_minWidth = newWidget(self,QLineEdit,"-1")
		self.edit_maxWidth = newWidget(self,QLineEdit,"-1")

		lb_rangeHeight = newWidget(self,QLabel,"rangeHeight")
		self.edit_minHeight = newWidget(self,QLineEdit,"-1")
		self.edit_maxHeight = newWidget(self,QLineEdit,"-1")

		lb_rangeArea = newWidget(self,QLabel,"rangeArea")
		self.edit_minArea = newWidget(self,QLineEdit,"-1")
		self.edit_maxArea = newWidget(self,QLineEdit,"-1")

		lb_kSizeBlur = newWidget(self,QLabel,"kSizeBlur")
		self.edit_kSizeBlur = newWidget(self,QLineEdit,"3")

		lb_kSizeMorph = newWidget(self,QLabel,"kSizeMorph")
		self.edit_kSizeMorph = newWidget(self,QLineEdit,"3")

		lb_iter = newWidget(self,QLabel,"iter")
		self.edit_iter = newWidget(self,QLineEdit,"1")

		advance = newButton(self,"Advance Settings",self.advance)
		apply_ = newButton(self,"Apply",self.apply)
		close_ = newButton(self,"Close",self.close)

		# group binary
		sub_layout = QGridLayout()

		sub_layout.addWidget(lb_thresh,0,0)
		sub_layout.addWidget(self.edit_thresh,0,1)

		sub_layout.addWidget(lb_blockSize,1,0)
		sub_layout.addWidget(self.edit_blockSize,1,1)

		sub_layout.addWidget(lb_c,2,0)
		sub_layout.addWidget(self.edit_c,2,1)

		group_binary.setLayout(sub_layout)

		# group remove contours
		sub_layout = QGridLayout()

		sub_layout.addWidget(lb_rangeWidth,0,0)
		sub_layout.addWidget(self.edit_minWidth,0,1)
		sub_layout.addWidget(self.edit_maxWidth,0,2)

		sub_layout.addWidget(lb_rangeHeight,1,0)
		sub_layout.addWidget(self.edit_minHeight,1,1)
		sub_layout.addWidget(self.edit_maxHeight,1,2)

		sub_layout.addWidget(lb_rangeArea,2,0)
		sub_layout.addWidget(self.edit_minArea,2,1)
		sub_layout.addWidget(self.edit_maxArea,2,2)

		group_removeContours.setLayout(sub_layout)

		# group blur,morphology
		sub_layout = QGridLayout()

		sub_layout.addWidget(lb_kSizeBlur,0,0)
		sub_layout.addWidget(self.edit_kSizeBlur,0,1)

		sub_layout.addWidget(lb_kSizeMorph,1,0)
		sub_layout.addWidget(self.edit_kSizeMorph,1,1)

		sub_layout.addWidget(lb_iter,2,0)
		sub_layout.addWidget(self.edit_iter,2,1)

		group_blurAndMorph.setLayout(sub_layout)

		#
		sub_layout = QVBoxLayout()
		sub_layout.addWidget(group_binary)
		sub_layout.addWidget(group_removeContours)
		sub_layout.addWidget(group_blurAndMorph)
		layout.addLayout(sub_layout)

		sub_layout = QHBoxLayout()
		sub_layout.addWidget(advance)
		sub_layout.addWidget(apply_)
		sub_layout.addWidget(close_)
		layout.addLayout(sub_layout)

		self.setLayout(layout)

	def advance(self):
		pass

	def apply(self):
		save_config("parameter.config",self.getConfig())

	def getConfig(self):
		config = ConfigParser()
		config["binary"] = {"k-thresh":self.edit_thresh.text(),
							"blockSize":self.edit_blockSize.text(),
							"C":self.edit_c.text()}

		config["removeContours"] = {"width":"%s,%s"%(self.edit_minWidth.text(),self.edit_maxWidth.text()),
									"height":"%s,%s"%(self.edit_minHeight.text(),self.edit_maxHeight.text()),
									"area":"%s,%s"%(self.edit_minArea.text(),self.edit_maxArea.text())}

		config["blur,morph"] = {"kSizeBlur":self.edit_kSizeBlur.text(),
							"kSizeMorph":self.edit_kSizeMorph.text(),
							"iter":self.edit_iter.text()}

		return config

	def __del__(self):
		del(self)