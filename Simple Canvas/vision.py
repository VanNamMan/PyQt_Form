import cv2
import numpy as np
from utils import str2ListInt,inSide,drawRect,drawText

class Remove:
    def __init__(self):
        self.boxs = []
        self.cnts = []
class Macth:
    def __init__(self):
        self.box   = None
        self.score = 0.0
        self.res   = False
 
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

def isGray(mat):
    return len(mat.shape) == 1 

def convert(mat,config):
    type_ = config["Convert"]["type"]
    if type_   == "bgr2gray":
        if isGray(mat):
            return mat
        return cv2.cvtColor(mat,cv2.COLOR_BGR2GRAY)
    elif type_ == "gray2bgr":
        if isGray(mat):
            return cv2.cvtColor(mat,cv2.COLOR_GRAY2BGR)
        else:
            return mat
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
    method       = config["Blur"]["method"]
    size         = int(config["Blur"]["size"])
    if method    == "blur":
        return cv2.blur(mat,(size,size))
    elif method  == "median":
        return cv2.medianBlur(mat,size)
    else:
        return cv2.GaussianBlur(mat,(size,size),0)

def morph(mat,config):
    method       = config["Morph"]["method"]
    size         = int(config["Morph"]["size"])
    iter         = int(config["Morph"]["iter"])
    kernel = np.ones((size,size),np.uint8) 
    if method    == "dilate":
        return cv2.dilate(mat,kernel,iterations=iter)
    elif method  == "erode":
        return cv2.erode(mat,kernel,iterations=iter)
    elif method  == "open":
        return cv2.morphologyEx(mat, cv2.MORPH_OPEN, kernel,iterations=iter)
    elif method  == "close":
        return cv2.morphologyEx(mat, cv2.MORPH_CLOSE, kernel,iterations=iter)
    elif method  == "gradient":
        return cv2.morphologyEx(mat, cv2.MORPH_GRADIENT, kernel,iterations=iter)
    elif method  == "top hat":
        return cv2.morphologyEx(mat, cv2.MORPH_TOPHAT, kernel,iterations=iter)
    elif method  == "black hat":
        return cv2.morphologyEx(mat, cv2.MORPH_BLACKHAT, kernel,iterations=iter)

def findContours(mat,config):
    mode                = config["Contours"]["mode"]
    method              = config["Contours"]["method"]
    if mode == "external":
        mode = cv2.RETR_EXTERNAL
    elif mode == "list":
        mode = cv2.RETR_LIST
    
    if method == "simple":
        method = cv2.CHAIN_APPROX_SIMPLE
    elif method == "none":
        method = cv2.CHAIN_APPROX_NONE

    _,cnts,_ = cv2.findContours(mat,mode,method)
    
    return cnts

def ocr(mat,config):
    
    pass
def matching(mat,config):
    score               = float(config["Matching"]["score"])
    file                = config["Matching"]["file"]
    method              = eval('cv2.TM_CCOEFF_NORMED')
    # if temp is None:
    temp                = cv2.imread(file,0)
    if not isGray(mat):
        img = cv2.cvtColor(mat,cv2.COLOR_BGR2GRAY)
    else:
        img = mat
    w0,h0               = temp.shape[:2][::-1]
    res                 = cv2.matchTemplate(img,temp,method)
    _,max_val,_,max_loc = cv2.minMaxLoc(res)

    res                 = Macth()
    res.box             = list(max_loc) + [w0,h0]
    res.score           = max_val
    res.res             = True if max_val > score/100 else False
    return res

def removeBlobs(cnts,config):
    width               = str2ListInt(config["Remove"]["width"])
    height              = str2ListInt(config["Remove"]["height"])
    area                = str2ListInt(config["Remove"]["area"])

    res = Remove()
    for cnt in cnts :
        x,y,w,h = cv2.boundingRect(cnt)
        if not inSide(w,width) : continue
        if not inSide(w,width) : continue
        if not inSide(w,width) : continue
        res.boxs.append([x,y,w,h])
        res.cnts.append(cnt)
    return res

function_tools = {
    "crop"             : crop, 
    "convert"          : convert,
    "binary"           : binary,
    "blur"             : blur,
    "morph"            : morph,
    "findContours"     : findContours,
    "ocr"              : ocr,
    "matching"         : matching,
    "removeBlobs"      : removeBlobs
}

def process(mat,lb_funcs,config
            ,draw_box=False,draw_match=False
            ,lw=2,fs=1,color=(0,255,0)):
    copy = mat.copy()
    dst = None
    for i,lb in enumerate(lb_funcs):
        if i == 0:
            dst = function_tools[lb](copy,config)
        else:
            dst = function_tools[lb](dst,config)

    if isinstance(dst,np.ndarray):
        return dst
    else:
        if "crop" in lb_funcs:
            x0,y0,_,_ = str2ListInt(config["Crop"]["box"])
        else:
            x0,y0 = 0,0
        if isinstance(dst,Remove) and draw_box:
            for box in dst.boxs:
                box[0]+=x0
                box[1]+=y0
                drawRect(copy,box,lw=lw,color=color)
        if isinstance(dst,Macth) and draw_match:
            res = dst.res
            box = dst.box
            box[0]+=x0
            box[1]+=y0
            x,y = box[:2]
            drawRect(copy,box,lw=lw,color=color)
            drawText(copy,"%s:%.2f"%(str(res),dst.score),(x,y))

        return copy
