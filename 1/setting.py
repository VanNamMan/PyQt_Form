from PyQt5.QtWidgets import QDialog,QSlider,QMenu
#from PyQt5.QtCore import Qt
from ui_setting import Ui_setting


import PyQt5.QtCore as QtCore


class Setting(QDialog):
    def __init__(self, parent):
        super(Setting, self).__init__(parent)
        #self.setWindowFlags(Qt.Window)
        self.ui = Ui_setting()
        self.ui.setupUi(self)

        [self.ui.cbb_modeFindcontours.addItem(item) for item in ["RETR_CCOMP","RETR_EXTERNAL","RETR_LIST","RETR_TREE"]]
        [self.ui.cbb_modeBlur.addItem(item) for item in ["BLUR_NORMAL","BLUR_GAUSS","BLUR_MEDIAN"]]
        [self.ui.cbb_methodFindcontours.addItem(item) for item in ["CHAIN_APPROX_NONE","CHAIN_APPROX_SIMPLE"
                                                                ,"CHAIN_APPROX_TC89_KCOS","CHAIN_APPROX_TC89_L1"]]
        [self.ui.cbb_modeMorphology.addItem(item) for item in ["MORPHO_DILATE","MORPHO_ERODE"]]
        [self.ui.cbb_modeThresh.addItem(item) for item in ["THRESH_BINARY","THRESH_BINARY_INV","THRESH_TOZERO"
                                                            ,"THRESH_TOZERO_INV","THRESH_TRIANGLE","THRESH_TRUNC"]]
        [self.ui.cbb_methodAdaptive.addItem(item) for item in ["ADAPTIVE_THRESH_GAUSSIAN_C","ADAPTIVE_THRESH_MEAN_C"]]

    def __del__(self):
        self.ui = None


    
        

    