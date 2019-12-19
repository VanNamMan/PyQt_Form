from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

from header.parameterUi import Ui_ParaDlg

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

class ParaDlg(QDialog):
    def __init__(self):
        super(ParaDlg,self).__init__()
        self.ui = Ui_ParaDlg()
        self.ui.setupUi(self)

        self.setLayout(self.ui.verticalLayout)

        tree1 = self.ui.treeParams
        tree2 = self.ui.treeCamera

        spin = QSpinBox(self)
        spin.setRange(0,255)
        addWidget(tree1,0,0,spin)
        addWidget(tree1,1,0,QLineEdit("3",self))
        addWidget(tree1,2,0,QLineEdit("3",self))
        addWidget(tree1,2,1,QLineEdit("1",self))
        addWidget(tree1,3,0,QLineEdit("-1,-1",self))
        addWidget(tree1,3,1,QLineEdit("-1,-1",self))
        addWidget(tree1,3,2,QLineEdit("-1,-1",self))

        spin2 = QSpinBox(self)
        spin2.setRange(0,100)
        addWidget(tree1,5,0,spin2)

        addWidget(tree1,0,1,newCbb(["normal","inv"],self))
        addWidget(tree1,0,2,newCbb(["normal","otsu","adaptive"],self))
        addWidget(tree1,1,1,newCbb(["blur","median","gauss"],self))
        addWidget(tree1,2,2,newCbb(["dilate","erode","close","open"],self))

        addWidget(tree1,4,0,newCbb(["%d"%i for i in range(4)],self))
        addWidget(tree1,4,1,newCbb(["%d"%i for i in range(14)],self))
        addWidget(tree1,4,2,newCbb(["eng","vie","kor"],self))

        addWidget(tree2,0,None,newCbb(["dino","basler"],self))
        addWidget(tree2,1,None,QLineEdit("...",self))
