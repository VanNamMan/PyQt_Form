from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from header.parameterUi import Ui_ParaDlg

from libs_.utils import*
from configparser import ConfigParser

def addItems(cbb,items):
    [cbb.addItem(it) for it in items]

def addWidget(tree,idIt,idChild,widget):
    if idChild is not None:
        it = tree.topLevelItem(idIt).child(idChild)
        tree.setItemWidget(it, 1, widget)
    else:
        it = tree.topLevelItem(idIt)
        tree.setItemWidget(it, 1, widget)

def newCbb(items,parent):
    cbb = QComboBox(parent)
    addItems(cbb,items)
    return cbb

class Items(object):
    def __init__(self,parent):
        spin = QSpinBox(parent)
        spin.setRange(0,255)
        spin.setValue(100)
        spin2 = QSpinBox(parent)
        spin2.setRange(0,100)
        spin2.setValue(90)
        self.binary_threshold = spin
        self.binary_type = newCbb(["normal","inv"],parent)
        self.binary_method = newCbb(["normal","otsu","adaptive"],parent)
        self.blur_size = QLineEdit("3",parent)
        self.blur_method = newCbb(["blur","median","gauss"],parent)
        self.morph_size = QLineEdit("3",parent)
        self.morph_iter = QLineEdit("1",parent)
        self.morph_method = newCbb(["dilate","erode","close","open"],parent)
        self.remove_width = QLineEdit("-1,-1",parent)
        self.remove_height = QLineEdit("-1,-1",parent)
        self.remove_area = QLineEdit("-1,-1",parent)
        self.orc_oem = newCbb(["%d"%i for i in range(4)],parent)
        self.orc_psm = newCbb(["%d"%i for i in range(14)],parent)
        self.orc_lang = newCbb(["eng","vie","kor"],parent)
        self.match_score = spin2
        self.camera_type = newCbb(["dino","basler"],parent)
        self.camera_id = QLineEdit("...",parent)

class ParaDlg(QDialog):
    def __init__(self):
        super(ParaDlg,self).__init__()
        self.ui = Ui_ParaDlg()
        self.ui.setupUi(self)

        self.setLayout(self.ui.verticalLayout)

        tree1 = self.ui.treeParams
        tree2 = self.ui.treeCamera

        self.items = Items(self)

        addWidget(tree1,0,0,self.items.binary_threshold)
        addWidget(tree1,0,1,self.items.binary_type)
        addWidget(tree1,0,2,self.items.binary_method)

        addWidget(tree1,1,0,self.items.blur_size)
        addWidget(tree1,1,1,self.items.blur_method)

        addWidget(tree1,2,0,self.items.morph_size)
        addWidget(tree1,2,1,self.items.morph_iter)
        addWidget(tree1,2,2,self.items.morph_method)

        addWidget(tree1,3,0,self.items.remove_width)
        addWidget(tree1,3,1,self.items.remove_height)
        addWidget(tree1,3,2,self.items.remove_area)

        addWidget(tree1,4,0,self.items.orc_oem)
        addWidget(tree1,4,1,self.items.orc_psm)
        addWidget(tree1,4,2,self.items.orc_lang)

        addWidget(tree1,5,0,self.items.match_score)

        addWidget(tree2,0,None,self.items.camera_type)
        addWidget(tree2,1,None,self.items.camera_id)

    def save(self):
        mkdir("Parameter")
        config = ConfigParser()

        pass
    def load(self):

        pass