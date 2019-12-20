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

class Keys(object):
    def __init__(self):
        self.binary = "binary"
        self.blur = "blur"
        self.morph = "morphology"
        self.remove = "removeBlobs"
        self.ocr = "ocr"
        self.match = "matching"
        self.camera = "camera"

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

class ParaDlg(QWidget):
    FOLDER = "Parameter"
    FILE_NAME = "Parameter/para.config"
    saveConfigSignal = pyqtSignal(bool)
    loadConfigSignal = pyqtSignal(bool)
    def __init__(self):
        super(ParaDlg,self).__init__()
        self.ui = Ui_ParaDlg()
        self.ui.setupUi(self)
        # 
        self.ui.but_save.clicked.connect(self.save)
        # 
        self.setLayout(self.ui.verticalLayout)

        tree1 = self.ui.treeParams
        tree2 = self.ui.treeCamera

        self.items = Items(self)
        self.keys = Keys()
        self.list_keys = [
            self.keys.binary,
            self.keys.blur,
            self.keys.morph,
            self.keys.remove,
            self.keys.ocr,
            self.keys.match,
            self.keys.camera
        ]

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

        # 
        self.config = ConfigParser()
        # 

    def save(self):
        try:
            mkdir(self.FOLDER)
            config = self.config
            config[self.keys.binary] = {
                "threshold":self.items.binary_threshold.text(),
                "type":self.items.binary_type.currentText(),
                "method":self.items.binary_method.currentText(),
            }
            config[self.keys.blur] = {
                "size":self.items.blur_size.text(),
                "method":self.items.blur_method.currentText(),
            }
            config[self.keys.morph] = {
                "size":self.items.morph_size.text(),
                "iter":self.items.morph_iter.text(),
                "method":self.items.morph_method.currentText(),
            }
            config[self.keys.remove] = {
                "width":self.items.remove_width.text(),
                "height":self.items.remove_height.text(),
                "area":self.items.remove_area.text(),
            }
            config[self.keys.ocr] = {
                "oem":self.items.orc_oem.currentText(),
                "psm":self.items.orc_psm.currentText(),
                "lang":self.items.orc_lang.currentText(),
            }
            config[self.keys.match] = {
                "score":self.items.match_score.text(),
            }
            config[self.keys.camera] = {
                "type":self.items.camera_type.currentText(),
                "id":self.items.camera_id.text(),
            }
            with open(self.FILE_NAME,"w") as cfgfile:
                config.write(cfgfile)
            
            print("parameter saved at %s"%self.FILE_NAME)
            self.saveConfigSignal.emit(True)

        except :
            print("parameter save fail")
            self.saveConfigSignal.emit(False)

    def load(self):
        if os.path.isfile(self.FILE_NAME):
            self.config.read(self.FILE_NAME)
            return True
        else:
            print("no such file %s"%self.FILE_NAME)
            self.loadConfigSignal.emit(False)
            return False
    
    def update(self):
        if self.load():
            try:
                binary = self.config[self.keys.binary]
                self.items.binary_threshold.setValue(int(binary["threshold"]))
                self.items.binary_type.setCurrentText(binary["type"])
                self.items.binary_method.setCurrentText(binary["method"])

                blur = self.config[self.keys.blur]
                self.items.blur_size.setText(blur["size"])
                self.items.blur_method.setCurrentText(binary["method"])
                
                morph = self.config[self.keys.morph]
                self.items.morph_size.setText(morph["size"])
                self.items.morph_iter.setText(morph["iter"])
                self.items.morph_method.setCurrentText(morph["method"])

                remove = self.config[self.keys.remove]
                self.items.remove_width.setText(remove["width"])
                self.items.remove_height.setText(remove["height"])
                self.items.remove_area.setText(remove["area"])

                ocr = self.config[self.keys.ocr]
                self.items.orc_oem.setCurrentText(ocr["oem"])
                self.items.orc_psm.setCurrentText(ocr["psm"])
                self.items.orc_lang.setCurrentText(ocr["lang"])

                match = self.config[self.keys.match]
                self.items.match_score.setValue(int(match["score"]))

                camera = self.config[self.keys.camera]
                self.items.camera_type.setCurrentText(camera["type"])
                self.items.camera_id.setText(camera["id"])
                
                print("Done load para")
                self.loadConfigSignal.emit(True)

            except :
                print("Load para fail")
                self.loadConfigSignal.emit(False)
            
