import cv2
import numpy as np

remove = {
    "boxs" : [],
    "mat"  : None
}

def str2ListInt(string):
    return [int(a) for a in string.split(",")]
 
class Result(object):
    def __init__(self):
        super(Result,self).__init__()
        self.crop     = None
        self.gray     = None
        self.bgr      = None
        self.binary   = None
        self.blur     = None
        self.morph    = None
        self.ocr      = ""
        self.matching = 0.0
        self.remove   = remove

def crop(mat,config):
    x,y,w,h = str2ListInt(config["Crop"]["box"])
    return mat[y:y+h,x:x+w]
    
def convert(mat,config):
    type_ = config["Convert"]["type"]
    if type_   == "bgr2gray":
        return cv2.cvtColor(mat,cv2.COLOR_BGR2GRAY)
    elif type_ == "gray2bgr":
        return cv2.cvtColor(mat,cv2.COLOR_GRAY2BGR)
    elif type_ == "hsv":
        if len(mat.shape) == 3:
            return cv2.cvtColor(mat,cv2.COLOR_BGR2HSV)
        else :
            return mat

def binary(mat,config):
    method       = config["Binary"]["method"]
    thresh       = int(config["Binary"]["threshold"])
    type_        = config["Binary"]["type"]
    blockSize    = int(config["Binary"]["blocksize"])
    if type_ == "normal":
        type_ = cv2.THRESH_BINARY
    elif type_ == "inv":
        type_ = cv2.THRESH_BINARY_INV
    if method == "normal":
        return cv2.threshold(mat,thresh,255,type_)[1]
    elif method == "otsu":
        return cv2.threshold(mat,thresh,255,type_|cv2.THRESH_OTSU)[1]
    elif method == "adaptive":
        return cv2.adaptiveThreshold(mat,255,cv2.ADAPTIVE_THRESH_MEAN_C,type_,blockSize,thresh)

def blur(mat,config):
    pass
def morph(mat,config):
    pass
def ocr(mat,config):
    pass
def matching(mat,config):
    pass
def remove(mat,config):
    pass

function_tools = {
    "crop"      : crop, 
    "convert"   : convert,
    "binary"    : binary,
    "blur"      : blur,
    "morph"     : morph,
    "ocr"       : ocr,
    "matching"  : matching,
    "remove"    : remove
}

def process(mat,lb_funcs,config):
    copy = mat.copy()
    dst = None
    for i,lb in enumerate(lb_funcs):
        if i == 0:
            dst = function_tools[lb](mat,config)
        else:
            dst = function_tools[lb](dst,config)
    
    return dst
