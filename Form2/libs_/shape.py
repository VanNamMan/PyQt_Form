from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class Shape(object):
    def __init__(self,rect):
        super(Shape).__init__()
        self.r = rect
        self.tl = rect[:2]
        self.tr = (rect[0]+rect[2],rect[1])
        self.bl = (rect[0],rect[1]+rect[3])
        self.br = (rect[0]+rect[2],rect[1]+rect[3])

        self.points = [self.tl,self.tr,self.bl,self.br]
        
        self.labels = []
