import cv2
import numpy as np
from utils import *
# function_tools = {
#     "crop"             : crop,                1
#     "convert"          : convert,             2
#     "binary"           : binary,              3
#     "blur"             : blur,                4
#     "morphology"       : morph,               5
#     "findContours"     : findContours,        6
#     "ocr"              : ocr,                 7
#     "matching"         : matching,            8
#     "removeBlobs"      : removeBlobs          9
# }

class Mat(object):
    def __init__(self,mat):
        self.__name__       = "mat"
        self.mat            = mat
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__ + " : " + str(self.mat.shape)
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return self.mat   
class Crop(object):
    def __init__(self):
        self.__name__       = "crop"
        self.mat            = None
        self.roi            = []
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__ + " : " + str(self.roi)
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return self.mat
class Convert(object):
    def __init__(self):
        self.__name__       = "convert"
        self.mat            = None
    def __out__(self):
        return self.mat  
    def __str__(self):
        text = self.__name__ 
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return toBgr(self.mat)
class Binary(object):
    def __init__(self):
        self.__name__       = "binary"
        self.mat            = None
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return toBgr(self.mat)
class Blur(object):
    def __init__(self):
        self.__name__       = "blur"
        self.mat            = None
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return toBgr(self.mat)
class Morph(object):
    def __init__(self):
        self.__name__       = "morphology"
        self.mat            = None
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return toBgr(self.mat)
class Cnts(object):
    def __init__(self):
        self.__name__       = "findContours"
        self.mat            = None
        self.cnts = []
    def __out__(self):
        return self.cnts
    def __getitem__(self,i):
        return self.cnts[i]
    def __len__(self):
        return len(self.cnts)
    def __str__(self):
        text = self.__name__ + " : %d"%len(self)
        for i in range(len(self)):
            text += "\n\t%d : %s"%(i,str(self[i].shape))
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return draw(self.mat,cnts=self.cnts)

class Remove(object):
    def __init__(self):
        self.__name__       = "removeBlobs"
        self.mat            = None
        self.boxs           = []
        self.cnts           = []
    def __out__(self):
        return self.boxs
    def __getitem__(self,i):
        return (self.boxs[i],self.cnts[i])
    def __len__(self):
        return len(self.boxs)
    def __str__(self):
        text = self.__name__ + " : %d"%len(self)
        for i in range(len(self)):
            box,cnt = self[i]
            text += "\n\t%d : %s , %s"%(i,str(box),str(cnt.shape))
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return draw(self.mat,boxs=self.boxs)

class OCR(object):
    def __init__(self):
        self.__name__       = "ocr"
        self.mat            = None
        self.text           = ""
    def __out__(self):
        return self.text
    def __str__(self):
        text = self.__name__ + " :\n" + self.text
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        return draw(self.mat,[self.text])

class Match(object):
    def __init__(self):
        self.__name__       = "matching"
        self.mat            = None
        self.boxs           = []
        self.scores         = []
        self.predicts       = []
    def __out__(self):
        return self.boxs
    def __getitem__(self,i):
        return (self.boxs[i],self.scores[i],self.predicts[i])
    def __len__(self):
        return len(self.boxs)
    def __str__(self):
        text = self.__name__ + " : %d"%len(self)
        # for i in range(len(self)):
        #     box,score,pred = self[i]
        #     string = "\n\t%d : %s box %s ,score %.2f"%(i,str(box),score)
        #     text += string
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        texts = ["%.2f"%s for s in self.scores]
        orgs = [(b[0],b[1]) for b in self.boxs]
        return draw(self.mat,boxs=self.boxs,texts=texts,orgs=orgs)
class Predict(object):
    def __init__(self):
        super(Predict,self).__init__()
        self.__name__       = "predict"
        self.result         = True
        self.mat            = None
    
    def __str__(self):
        text = self.__name__ + ": " +str(self.result)
        return "***** %s *****"%text
    def visualize(self,pprint=False):
        if pprint:
            print(self)
        h,w                 = self.mat.shape[:2]
        org                 = (w//2,h//2)
        return draw(self.mat,texts=["%s"%str(self.result)],orgs=[org])

def isGray(mat):
    return len(mat.shape) == 2
def toBgr(mat):
    if isGray(mat):
        return cv2.cvtColor(mat,cv2.COLOR_GRAY2BGR)
    else:
        return mat

def crop(src,config):
    mat     = src.__out__()
    cfg     = config["crop"]
    x,y,w,h = str2ListInt(cfg["Box"])

    res     = Crop()
    res.mat = mat[y:y+h,x:x+w]
    res.roi = [x,y,w,h]
    return res
 
def convert(src,config):
    mat         = src.__out__()
    cfg         = config["convert"]
    type_       = cfg["Type"]
    res         = Convert()
    if type_   == "bgr2gray":
        if isGray(mat):
            res.mat = mat
        res.mat = cv2.cvtColor(mat,cv2.COLOR_BGR2GRAY)

    elif type_ == "gray2bgr":
        if isGray(mat):
            res.mat = cv2.cvtColor(mat,cv2.COLOR_GRAY2BGR)
        else:
            res.mat = mat

    elif type_ == "hsv":
        if len(mat.shape) == 3:
            res.mat = cv2.cvtColor(mat,cv2.COLOR_BGR2HSV)
        else :
            res.mat = mat
    return res

def binary(src,config):
    mat          = src.__out__()
    cfg          = config["binary"]
    method       = cfg["Method"]
    thresh       = int(cfg["Threshold"])
    type_        = cfg["Type"]
    blockSize    = int(cfg["BlockSize"])
    res          = Binary()
    if type_    == "normal":
        type_   = cv2.THRESH_BINARY
    elif type_  == "inv":
        type_   = cv2.THRESH_BINARY_INV
    if method   == "normal":
        res.mat = cv2.threshold(mat,thresh,255,type_)[1]
    elif method == "otsu":
        res.mat = cv2.threshold(mat,thresh,255,type_|cv2.THRESH_OTSU)[1]
    elif method == "adaptive":
        res.mat = cv2.adaptiveThreshold(mat,255,cv2.ADAPTIVE_THRESH_MEAN_C,type_,blockSize,thresh)
    return res

def blur(src,config):
    mat          = src.__out__()
    cfg          = config["blur"]
    method       = cfg["Method"]
    size         = int(cfg["Size"])
    res          = Blur()
    if method    == "blur":
        res.mat  = cv2.blur(mat,(size,size))
    elif method  == "median":
        res.mat  = cv2.medianBlur(mat,size)
    else:
        res.mat  = cv2.GaussianBlur(mat,(size,size),0)
    return res

def morph(src,config):
    mat          = src.__out__()
    cfg          = config["morph"]
    method       = cfg["Method"]
    size         = int(cfg["Size"])
    iter         = int(cfg["Iter"])
    kernel       = np.ones((size,size),np.uint8) 
    res          = Morph()
    if method    == "dilate":
        res.mat  = cv2.dilate(mat,kernel,iterations=iter)
    elif method  == "erode":
        res.mat  = cv2.erode(mat,kernel,iterations=iter)
    elif method  == "open":
        res.mat  = cv2.morphologyEx(mat, cv2.MORPH_OPEN, kernel,iterations=iter)
    elif method  == "close":
        res.mat  = cv2.morphologyEx(mat, cv2.MORPH_CLOSE, kernel,iterations=iter)
    elif method  == "gradient":
        res.mat  = cv2.morphologyEx(mat, cv2.MORPH_GRADIENT, kernel,iterations=iter)
    elif method  == "top hat":
        res.mat  = cv2.morphologyEx(mat, cv2.MORPH_TOPHAT, kernel,iterations=iter)
    elif method  == "black hat":
        res.mat  = cv2.morphologyEx(mat, cv2.MORPH_BLACKHAT, kernel,iterations=iter)
    return res

def findContours(src,config):
    mat             = src.__out__()
    cfg             = config["contours"]
    mode            = cfg["Mode"]
    method          = cfg["Method"]
    res             = Cnts()
    if mode         == "external":
        mode        = cv2.RETR_EXTERNAL
    elif mode       == "list":
        mode        = cv2.RETR_LIST
    
    if method       == "simple":
        method      = cv2.CHAIN_APPROX_SIMPLE
    elif method     == "none":
        method      = cv2.CHAIN_APPROX_NONE

    if cv2.__version__ > "3":
      res.cnts,_        = cv2.findContours(mat,mode,method)
    else:  
        _,res.cnts,_    = cv2.findContours(mat,mode,method)
    res.mat         = mat
    return res

def removeBlobs(src,config):
    cnts                = src.__out__()
    cfg                 = config["remove"]
    width               = str2ListInt(cfg["Width"])
    height              = str2ListInt(cfg["Height"])
    area                = str2ListInt(cfg["Area"])
    res                 = Remove()
    for cnt in cnts :
        x,y,w,h         = cv2.boundingRect(cnt)
        s               = cv2.contourArea(cnt)
        if not inSide(w,width) : continue
        if not inSide(h,width) : continue
        if not inSide(s,area) : continue
        res.boxs.append([x,y,w,h])
        res.cnts.append(cnt)
    res.mat             = src.mat
    return res

def ocr(src,config):
    mat         = src.mat
    cfg         = config["ocr"]
    lang        = cfg["Lang"]
    oem         = cfg["Oem"]
    psm         = cfg["Psm"]
    ocr_config  = "-l %s --oem %s --psm %s"%(lang,oem,psm)
    res         = OCR()
    res.text    = ocr_(mat,ocr_config)
    res.mat     = mat
    return res

def matching(src,config):
    mat                 = src.__out__()
    cfg                 = config["matching"]
    score               = float(cfg["Score"])/100
    file                = cfg["File"]
    multiple            = eval(cfg["Multiple"])
    method              = cv2.TM_CCOEFF_NORMED
    res                 = Match()
    # if temp is None:
    temp                = cv2.imread(file,0)
    if not isGray(mat):
        img = cv2.cvtColor(mat,cv2.COLOR_BGR2GRAY)
    else:
        img = mat
    
    w0,h0               = temp.shape[:2][::-1]
    result              = cv2.matchTemplate(img,temp,method)
    
    
    if not multiple:
        _,max_val,_,max_loc = cv2.minMaxLoc(result)

        res.boxs            = [list(max_loc) + [w0,h0]]
        res.scores          = [max_val]
        res.predicts        = [True if max_val > score else False]
    else:
        res.boxs        = []
        res.scores      = []
        res.predicts    = []
        loc = np.where( result >= score)
        for pt in zip(*loc[::-1]):
            x,y = pt
            res.boxs.append([x,y,w0,h0])
            res.scores.append(result[y,x])
            res.predicts.append(True)
    res.mat         = mat
    #  sorting boxs
    _ , C        = sort_matching(res.boxs,res.scores,epsilon=50)

    res.boxs        = []
    res.scores      = []
    for key,val in C.items():
        b,s = val[-1]
        res.boxs.append(b)
        res.scores.append(s)
    return res

def predict(src,config):
    mat         = src.mat

DEF_FONT    = cv2.FONT_HERSHEY_COMPLEX      
DEF_POS     = [(50,100)]
DEF_COLOR   = (0,255,0)
DEF_LW      = 2
DEF_FS      = 2
DEF_LB_FUNCTIONS    = readline("default_function.txt")
DEF_FUNCTIONS       = [crop,convert,blur,binary,
                            morph,findContours,removeBlobs,ocr,matching]
DEF_FUNCTION_TOOLS = {}
for lb,func in zip(DEF_LB_FUNCTIONS,DEF_FUNCTIONS):
    DEF_FUNCTION_TOOLS[lb]  = func

def draw(mat,texts=[],boxs=[],cnts=None
            ,idx    = -1
            ,orgs   = DEF_POS
            ,font   = DEF_FONT
            ,fs     = DEF_FS
            ,lw     = DEF_LW
            ,c      = DEF_COLOR):
    if isGray(mat):
        mat = cv2.cvtColor(mat,cv2.COLOR_GRAY2BGR)
    for text,org in zip(texts,orgs):
        cv2.putText(mat,text,org,font,fs,c,lw)
    for box in boxs:
        x,y,w,h = box
        cv2.rectangle(mat,(x,y),(x+w,y+h),c,lw)
    if cnts is not None:
        cv2.drawContours(mat,cnts,idx,c,lw)
    return mat

def test_process(mat,config
                ,color=(0,255,0)):
    # ======================
    dst         = Mat(mat)
    lb_funcs    = config["function"]["Functions"].split(",")
    keys        = list(DEF_FUNCTION_TOOLS.keys())
    results     = []
    visualizes  = []
    # ======================
    start = time.time()
    for i,lb in enumerate(lb_funcs):
        if lb not in keys:
            print("Dont suport \"%s\" funtion"%lb)
        else:
            try:
                t0 = time.time()
                dst           = DEF_FUNCTION_TOOLS[lb](dst,config)
                visualizes.append(dst.visualize(True))
                dt        = (time.time()-t0)*1000
                print("%s : %d ms"%(lb,dt))
                results.append(dst)
            except:
                print("has a problem at %s"%lb)
    end = time.time()
    dt = (end-start)*1000
    print("time inferenc : %d ms"%dt)
    # ======================     
    return results,visualizes

def configProxy2dict(config):
    dict_ = {}
    for key in config.keys():
        dict_[key] = eval(config[key])
    return dict_

def sort_matching(boxs,scores,epsilon=10):
    """
    sorting and romve near boxs
    """
    def key_box(box):
        return np.sqrt(box[0]**2+box[1]**2)
    def key_score(x):
        return x[1]
    boxs = sorted(boxs,key=key_box)
    i = 0
    B = [(boxs[0],scores[0])]
    C = {
        0:[(boxs[0],scores[0])]
    }
    for j in range(len(boxs)):
        tl1 = boxs[i][:2]
        tl2 = boxs[j][:2]
        b,s = boxs[j],scores[j]
        if  distance(tl2,tl1) > epsilon:
            B.append((b,s))
            C[len(C)]    = [(b,s)]
            i            = j
        else:
            C[len(C)-1].append((b,s))
    
    for key,val in C.items():
        val     = sorted(val,key=key_score)
        C[key]  = val

    return B,C

if __name__ == "__main__":
    
    pass
    # config      = ConfigParser()
    # config.read("demo/para.config")
    # config      = config["shape-0"]
    # config      = configProxy2dict(config)
    # print(config["function"]["Functions"])
    # mat         = cv2.imread("demo/1.jpg")
    # m = Mat(mat)
    # out = draw(m.mat,boxs=[[0,0,500,500]],lw=8)
    # cv2.imwrite("mat.png",m.mat)
    # t0          = time.time()
    # res,vis     = test_process(mat,config)
    # dt          = (time.time()-t0)*1000
    # print("time inference : %d"%(dt))
    # wd          = cv2.namedWindow("",cv2.WINDOW_FREERATIO)
    # # for v in vis:
    # cv2.imshow("",out)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()