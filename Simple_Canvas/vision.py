import cv2
import numpy as np
from utils import *

# function_tools = {
#     "crop"             : crop, 
#     "convert"          : convert,
#     "binary"           : binary,
#     "blur"             : blur,
#     "morphology"       : morph,
#     "findContours"     : findContours,
#     "ocr"              : ocr,
#     "matching"         : matching,
#     "removeBlobs"      : removeBlobs
# }

class OCR(object):
    def __init__(self):
        self.text = ""
class Remove:
    def __init__(self):
        self.boxs = []
        self.cnts = []
class Macth:
    def __init__(self):
        self.boxs   = None
        self.scores = 0.0
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
    cfg     = config["crop"]
    x,y,w,h = str2ListInt(cfg["Box"])
    return mat[y:y+h,x:x+w]

def isGray(mat):
    return len(mat.shape) == 1 

def convert(mat,config):
    cfg         = config["convert"]
    type_ = cfg["Type"]
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
    cfg          = config["binary"]
    method       = cfg["Method"]
    thresh       = int(cfg["Threshold"])
    type_        = cfg["Type"]
    blockSize    = int(cfg["BlockSize"])
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
    cfg          = config["blur"]
    method       = cfg["Method"]
    size         = int(cfg["Size"])
    if method    == "blur":
        return cv2.blur(mat,(size,size))
    elif method  == "median":
        return cv2.medianBlur(mat,size)
    else:
        return cv2.GaussianBlur(mat,(size,size),0)

def morph(mat,config):
    cfg          = config["morph"]
    method       = cfg["Method"]
    size         = int(cfg["Size"])
    iter         = int(cfg["Iter"])
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
    cfg                 = config["contours"]
    mode                = cfg["Mode"]
    method              = cfg["Method"]
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
    cfg         = config["ocr"]
    lang        = cfg["Lang"]
    oem         = cfg["Oem"]
    psm         = cfg["Psm"]
    ocr_config  = "-l %s --oem %s --psm %s"%(lang,oem,psm)
    res         = OCR()
    res.text    = ocr_(mat,ocr_config)
    return res

def matching(mat,config):
    cfg                 = config["matching"]
    score               = float(cfg["Score"])/100
    file                = cfg["File"]
    multiple            = eval(cfg["Multiple"])
    method              = cv2.TM_CCOEFF_NORMED
    # if temp is None:
    temp                = cv2.imread(file,0)
    if not isGray(mat):
        img = cv2.cvtColor(mat,cv2.COLOR_BGR2GRAY)
    else:
        img = mat
    
    w0,h0               = temp.shape[:2][::-1]
    result              = cv2.matchTemplate(img,temp,method)
    
    res                 = Macth()
    if not multiple:
        _,max_val,_,max_loc = cv2.minMaxLoc(result)

        res.boxs            = [list(max_loc) + [w0,h0]]
        res.scores          = [max_val]
        res.res             = [True if max_val > score else False]
    else:
        res.boxs   = []
        res.scores = []
        res.res    = []
        loc = np.where( result >= score)
        for pt in zip(*loc[::-1]):
            x,y = pt
            res.boxs.append([x,y,w0,h0])
            res.scores.append(result[y,x])
            res.res.append(True)

    return res

def removeBlobs(cnts,config):
    cfg                 = config["remove"]
    width               = str2ListInt(cfg["Width"])
    height              = str2ListInt(cfg["Height"])
    area                = str2ListInt(cfg["Area"])

    res = Remove()
    for cnt in cnts :
        x,y,w,h = cv2.boundingRect(cnt)
        s       = cv2.contourArea(cnt)
        if not inSide(w,width) : continue
        if not inSide(h,width) : continue
        if not inSide(s,area) : continue
        res.boxs.append([x,y,w,h])
        res.cnts.append(cnt)
    return res


lb_funcs                = readline("default_function.txt")
functions               = [crop,convert,blur,binary,
                            morph,findContours,removeBlobs,ocr,matching]
function_tools          = {}
for lb,func in zip(lb_funcs,functions):
    function_tools[lb]  = func

def test_process(mat,config
                ,draw_box=False
                ,draw_match=False
                ,color=(0,255,0)
                ,fs=1,lw=2):
    copy     = mat.copy()
    dst      = None
    lb_funcs = config["function"]["functions"].split(",")
    for i,lb in enumerate(lb_funcs):
        try:
            if i == 0:
                dst = function_tools[lb](copy,config)
            else:
                dst = function_tools[lb](dst,config)
        except:
            print("has a problem at %s"%lb)

    if isinstance(dst,np.ndarray):
        return dst
    else:
        if "crop" in lb_funcs:
            x0,y0,_,_ = str2ListInt(config["crop"]["Box"])
        else:
            x0,y0 = 0,0
        if isinstance(dst,Remove) and draw_box:
            for box in dst.boxs:
                box[0]+=x0
                box[1]+=y0
                drawRect(copy,box,lw=lw,color=color)
        if isinstance(dst,Macth) and draw_match:
            res     = dst.res
            scores  = dst.scores
            boxs    = dst.boxs
            for res_,score,box in zip(res,scores,boxs):
                box[0]+=x0
                box[1]+=y0
                x,y = box[:2]
                drawRect(copy,box,lw=lw,color=color)
                drawText(copy,"%s:%.2f"%(str(res_),score),(x,y),fs=fs,lw=lw)
        if isinstance(dst,OCR):
            return dst

        return copy
