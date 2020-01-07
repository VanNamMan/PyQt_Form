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
LESS_THAN = 0
MORE_THAN = 1
AS        = 2

MAT_START = 0
MAT_END   = -1


class Font(object):
    def __init__(self):
        self.fs = 2.0
        self.lw = 2
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.color = (255,0,0)
        self.NG_Color = (0,0,255)
        self.OK_Color = (0,255,0)
        self.cntColor = (0,255,255)
        self.pointColor = (0,0,255)
cvFont = Font()

class Mat(object):
    __checkin__    = np.ndarray
    __checkout__   = np.ndarray
    def __init__(self,mat):
        self.__name__       = "mat"
        self.mat            = mat
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__ + " : " + str(self.mat.shape)
        return "***** %s *****"%text
    def visualize(self,pprint=False,log=True,res=None):
        if pprint:
            print(self)
        # if log
        return gray2bgr(self.mat)

class Crop(object):
    __checkin__    = np.ndarray
    __checkout__   = np.ndarray
    def __init__(self):
        self.__name__       = "crop"
        self.mat            = None
        self.roi            = []
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__ + " : " + str(self.roi)
        return "***** %s *****"%text
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is not None:
            return gray2bgr(mat)
        else:
            return gray2bgr(self.mat)

class Convert(object):
    __checkin__    = np.ndarray
    __checkout__   = np.ndarray
    def __init__(self):
        self.__name__       = "convert"
        self.mat            = None
    def __out__(self):
        return self.mat  
    def __str__(self):
        text = self.__name__ 
        return "***** %s *****"%text
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is not None:
            return gray2bgr(mat)
        else:
            return gray2bgr(self.mat)
class Binary(object):
    __checkin__    = np.ndarray
    __checkout__   = np.ndarray
    def __init__(self):
        self.__name__       = "binary"
        self.mat            = None

    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__
        return "***** %s *****"%text
    def visualize(self,mat,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is not None:
            return gray2bgr(mat)
        else:
            return gray2bgr(self.mat)
class Blur(object):
    __checkin__    = np.ndarray
    __checkout__   = np.ndarray
    def __init__(self):
        self.__name__       = "blur"
        self.mat            = None
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__
        return "***** %s *****"%text
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is not None:
            return gray2bgr(mat)
        else:
            return gray2bgr(self.mat)
class Morph(object):
    __checkin__    = np.ndarray
    __checkout__   = np.ndarray
    def __init__(self):
        self.__name__       = "morphology"
        self.mat            = None

    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__
        return "***** %s *****"%text
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is not None:
            return gray2bgr(mat)
        else:
            return gray2bgr(self.mat)
class Contours(object):
    __checkin__    = np.ndarray
    __checkout__   = list
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
        # for i in range(len(self)):
        #     text += "\n\t%d : %s"%(i,str(self[i].shape))
        return "***** %s *****"%text
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is not None:
            return drawing(mat,cnts=self.cnts)
        else:
            return drawing(self.mat,cnts=self.cnts)

class Remove(object):
    __checkin__    = list
    __checkout__   = list
    def __init__(self):
        self.__name__       = "removeBlobs"
        self.mat            = None
        self.boxs           = []
        self.cnts           = []
        self.preds          = []

    def __out__(self):
        return self.boxs
    def __getitem__(self,i):
        return (self.boxs[i],self.cnts[i])
    def __len__(self):
        return len(self.boxs)
    def __str__(self):
        text = self.__name__ + " : %d"%len(self)
        # for i in range(len(self)):
            # box,cnt = self[i]
            # text += "\n\t%d : %s , %s"%(i,str(box),str(cnt.shape))
        return "***** %s *****"%text
    
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is None:
            return drawing(mat=self.mat,boxs=self.boxs,res=res)
        else:
            return drawing(mat,boxs=self.boxs,res=res)
class ConvexHull(object):
    __checkin__    = list
    __checkout__   = list
    def __init__(self):
        self.__name__       = "convexHull"
        self.mat            = None
        self.convexs        = []
        self.points         = []
        self.distances      = []

    def __out__(self):
        return self.convexs
    def __getitem__(self,i):
        return self.convexs[i],self.points[i],self.distances[i]
    def __len__(self):
        return len(self.convexs)
    def __str__(self):
        text = self.__name__ + " %d:\n"%len(self)
        return "***** %s *****"%text
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        
        if mat is None:
            mat = self.mat

        mat = drawing(mat,cnts=self.convexs,idx=-1)
        for points in self.points:
            radius = len(points)*[5]
            mat = drawing(mat,points=points,radius=radius)
        
        return mat

class OCR(object):
    __checkin__    = np.ndarray
    __checkout__   = str
    def __init__(self):
        self.__name__       = "ocr"
        self.mat            = None
        self.text           = ""

    def __out__(self):
        return self.text
    def __str__(self):
        text = self.__name__ + " :\n" + self.text
        return "***** %s *****"%text
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is None:
            return drawing(self.mat,[self.text])
        else:
            return drawing(mat,[self.text])

class Match(object):
    __checkin__    = np.ndarray
    __checkout__   = list
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
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        texts = ["%.2f"%s for s in self.scores]
        orgs = [(b[0],b[1]) for b in self.boxs]
        if mat is None:
            return drawing(self.mat,boxs=self.boxs,texts=texts,orgs=orgs)
        else:
            return drawing(mat,boxs=self.boxs,texts=texts,orgs=orgs)

class InRange(object):
    __checkin__    = np.ndarray
    __checkout__   = np.ndarray
    def __init__(self):
        self.__name__       = "inRange"
        self.mat            = None
    def __out__(self):
        return self.mat
    def __str__(self):
        text = self.__name__
        return text
    def visualize(self,mat=None,pprint=False,res=None):
        if pprint:
            print(self)
        if mat is not None:
            return gray2bgr(mat)
        else:
            return gray2bgr(self.mat)

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
        return drawing(self.mat,texts=["%s"%str(self.result)],orgs=[org])

def isGray(mat):
    return len(mat.shape) == 2

def crop(src:Mat,config)->Mat:
    """
    :src : Mat
    :dst : Mat 
    return cropped mat in roi
    """
    mat     = src.__out__()
    cfg     = config["crop"]
    x,y,w,h = str2ListInt(cfg["Box"])

    res     = Crop()
    res.mat = mat[y:y+h,x:x+w]
    res.roi = [x,y,w,h]
    return res
 
def convert(src:Mat,config)->Mat:
    """
    :src : Mat
    :dst : Mat
    return convert mat (bgr2gray,gray2bgr,bgr2hsv)
    """
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

def binary(src:Mat,config)->Mat:
    """
    :src : Mat
    :dst : Mat
    ***if otsu mode and binary mode: src must be binary mat***
    return binary mat
    """
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
        gray    = bgr2gray(mat)
        res.mat = cv2.threshold(gray,thresh,255,type_|cv2.THRESH_OTSU)[1]
    elif method == "adaptive":
        gray    = bgr2gray(mat)
        res.mat = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,type_,blockSize,thresh)
    return res

def blur(src:Mat,config)->Mat:
    """
    :src : Mat
    :dst : Mat
    return bluring mat
    """
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

def morph(src:Mat,config)->Mat:
    """
    :src : Mat
    :dst : Mat
    return morphology mat
    """
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

def findContours(src:Mat,config)->Contours:
    """
    :src : Mat 
    :dst : Contours <cnts>
    *** src must be binary mat ***
    """
    mat             = src.__out__()
    cfg             = config["contours"]
    mode            = cfg["Mode"]
    method          = cfg["Method"]
    res             = Contours()
    if mode         == "external":
        mode        = cv2.RETR_EXTERNAL
    elif mode       == "list":
        mode        = cv2.RETR_LIST
    
    if method       == "simple":
        method      = cv2.CHAIN_APPROX_SIMPLE
    elif method     == "none":
        method      = cv2.CHAIN_APPROX_NONE
    if cv2.__version__ > "4":
        res.cnts,_    = cv2.findContours(mat,mode,method)
    else:
        _,res.cnts,_    = cv2.findContours(mat,mode,method)
        # print(res.cnts[0].shape)
    res.mat         = mat
    return res

def removeBlobs(src:Contours,config)->Remove:
    """
    :src : list array [(None,1,2),...] 
    :dst : Remove <boxs>
    *** remove contour by width , height buondingBox or areaContour ***
    """
    cnts                = src.__out__()
    cfg                 = config["remove"]
    width               = str2ListInt(cfg["Width"])
    height              = str2ListInt(cfg["Height"])
    area                = str2ListInt(cfg["Area"])
    res                 = Remove()
    res.mat             = src.mat

    # 
    # predict_mean                = config["decision"]["Mean"]["state"]
    # predict_countNoneZero       = config["decision"]["CountNoneZero"]["state"]
    # predict_remove              = config["decision"]["Remove"]["state"]

    # compare_mean                = 0
    # compare_countNoneZero       = 0
    # compare_remove              = 0
    # 
    for cnt in cnts :
        x,y,w,h         = cv2.boundingRect(cnt)
        s               = cv2.contourArea(cnt)
        if not inSide(w,width) : continue
        if not inSide(h,height) : continue
        if not inSide(s,area) : continue
        res.boxs.append([x,y,w,h])
        res.cnts.append(cnt)
        # =========predict========
        # if predict_mean:
        #     roi             = src.mat[y:y+h,x:x+w]
        #     compare_type    = config["decision"]["Mean"]["compare"]
        #     value           = config["decision"]["Mean"]["value"]
        #     thrteshold      = config["decision"]["Mean"]["thrteshold"]
        #     m,_             = meanStd(roi)
        #     compare_mean    = distance(m,value)
        #     if compare_type:
        #         if compare_mean <= thrteshold:
        #             res.preds.append(False)
        #         else: 
        #             res.preds.append(True)
        #     if compare_type:
        #         if compare_mean <= thrteshold:
        #             res.preds.append(False)
        #         else: 
        #             res.preds.append(True)
        # =================
    
    return res

def ocr(src:Mat,config)->OCR:
    """
    :src : Mat
    :dst : OCR <text>
    *** read text from image (recommend : binary image)***
    """
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

def matching(src:Mat,config)->Match:
    """
    :src : Mat
    :dst : Macth <boxs,scores,predicts>
    *** matching temp mat in other mat***
    """
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
        boxs        = []
        scores      = []
        res.predicts    = []
        loc = np.where( result >= score)
        for pt in zip(*loc[::-1]):
            x,y = pt
            boxs.append([x,y,w0,h0])
            scores.append(result[y,x])
            res.predicts.append(True)

        #  sorting boxs , find boxs max score
        C        = sort_matching(boxs,scores,epsilon=50)

        res.boxs        = []
        res.scores      = []
        for key,val in C.items():
            b,s = val[-1]
            res.boxs.append(b)
            res.scores.append(s)

    res.mat         = mat
    return res

def inrange(src,config):
    """
    :src : Mat
    :return mask inRange HSV
    """
    mat = src.mat
    dst = InRange()
    
    if isGray(mat):
        return mat
    
    h,H = config["inrange"]["H"]
    s,S = config["inrange"]["S"]
    v,V = config["inrange"]["V"]

    hsv = cv2.cvtColor(mat, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower = np.array([h,s,v])
    upper = np.array([H,S,V])
    # Threshold the HSV image to get only colors
    dst.mat = cv2.inRange(hsv, lower, upper)

    return dst

def convexHull(src:Contours,config):
    """
    :src : Contours or Remove
    :return convex of cnt in contours
    """
    if isinstance(src,Remove):
        cnts = src.cnts 
    else:
        cnts = src.__out__()
    dst = ConvexHull()
    dst.mat = src.mat
    dst.convexs = []
    dst.points = []
    dst.distances = []
    for i in range(len(cnts)):
        points = []
        dis = []
        hull = cv2.convexHull(cnts[i],returnPoints=False)
        # hull_cnt = []
        defects = cv2.convexityDefects(cnts[i],hull)
        if defects is not None:
            for j in range(defects.shape[0]):
                s,e,f,d = defects[j,0]
                far = tuple(cnts[i][f][0])
                dis.append(d)
                points.append(far)
            

            hull_cnt = cnts[i][hull[:,0]]
            argmax = np.argmax(dis)
            dst.points.append(points)
            dst.distances.append(dis)
            dst.convexs.append(hull_cnt)

    return dst

#  ================
def draw(font   = cvFont
        ,mat    = None
        ,texts  =[]
        ,boxs   =[]
        ,cnts   =None
        ,idx    = -1
        ,orgs   = [(20,20)]
        ,points = []
        ,radius = []
        ,res    = None
        ):

    font        = cvFont.font
    fs          = cvFont.fs

    color       = cvFont.color
    lw          = cvFont.lw

    cntColor    = cvFont.cntColor
    pColor      = cvFont.pointColor

    if isGray(mat):
        mat = cv2.cvtColor(mat,cv2.COLOR_GRAY2BGR)
    for text,org in zip(texts,orgs):
        cv2.putText(mat,text,org,font,fs,color,lw)
    for box in boxs:
        x,y,w,h = box
        cv2.rectangle(mat,(x,y),(x+w,y+h),color,lw)
    if cnts is not None:
        cv2.drawContours(mat,cnts,idx,cntColor,lw)
    for p,r in zip(points,radius):
        cv2.circle(mat,p,r,pColor,thickness=-1)

    if res is None:
        pass
    elif res:
        cv2.rectangle(mat,(0,0),tuple(mat.shape[:2][::-1]),cvFont.OK_Color,3*lw)
    else:
        cv2.rectangle(mat,(0,0),tuple(mat.shape[:2][::-1]),cvFont.NG_Color,3*lw)
    return mat

# 
drawing = partial(draw,cvFont)
# 

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
    # B = [(boxs[0],scores[0])]
    C = {
        0:[(boxs[0],scores[0])]
    }
    for j in range(len(boxs)):
        tl1 = boxs[i][:2]
        tl2 = boxs[j][:2]
        b,s = boxs[j],scores[j]
        if  distance(tl2,tl1) > epsilon:
            # B.append((b,s))
            C[len(C)]    = [(b,s)]
            i            = j
        else:
            C[len(C)-1].append((b,s))
    
    for key,val in C.items():
        val     = sorted(val,key=key_score)
        C[key]  = val

    return C
def meanStd(mat):
    mean,std = cv2.meanStdDev(mat)
    return np.squeeze(mean),np.squeeze(std)

def gray2bgr(mat):
    if not isGray(mat):
        return mat
    else:
        return cv2.cvtColor(mat,cv2.COLOR_GRAY2BGR)
def bgr2gray(mat):
    if isGray(mat):
        return mat
    else:
        return cv2.cvtColor(mat,cv2.COLOR_BGR2GRAY)
def isBinary(mat):
    a255 = np.where(mat==255)[0]
    a0 = np.where(mat==0)[0]
    n = len(a255) + len(a0)

    if n == len(mat.ravel()) :
        return True
    else :
        return False
def checkin(funcs,mat):
    _in = Mat
    res = True
    msg = ""
    for i in range(len(funcs)):
        key  = eval(funcs[i])
        res  = key.__checkin__ == _in.__checkout__
        _in  = key
        if res : continue
        msg = "input not match at %s"%(key.__qualname__)
        return False,msg
    msg = "all functions macthing complete"
    return True,msg

# 
_MAT  = [eval(x) for x in ["Crop","Binary","Convert","Blur"]]
_LIST = [eval(x) for x in ["Remove"]]
# 
def decision_meanGray(results,config=None,threshold=100):
    boxs = results[-1].__out__()
    mat  = results[1].mat
    for x,y,w,h in boxs:
        roi = mat[y:y+h,x:x+w]
        m,_ = meanStd(roi)
    return True
    

def decision_meanBGR(results,config):
    pass
    

# =========deffine functions==============
DEF_FUNCTIONS       = {Crop         : crop ,
                       Convert      : convert,
                       Blur         : blur,
                       Binary       : binary,
                       Morph        : morph,
                       Contours     : findContours,
                       Remove       : removeBlobs,
                       OCR          : ocr,
                       Match        : matching,
                       InRange      : inrange,
                       ConvexHull   : convexHull}
# =====================================

def test_process(mat,config,bTeaching=True,pprint=True
                ,color=(0,255,0)):
    # ======================
    dst         = Mat(mat)
    lb_funcs    = config["function"]["Functions"].split(",")
    # decision    = config["decision"]
    keys        = list(DEF_FUNCTIONS.keys())
    results     = []
    visualizes  = []
    # ======================
    start = time.time()
    for i,lb in enumerate(lb_funcs):
        if lb and eval(lb) not in keys:
            print("Dont suport \"%s\" funtion"%lb)
        else:
            # try:
                t0 = time.time()
                dst           = DEF_FUNCTIONS[eval(lb)](dst,config)
                dt            = (time.time()-t0)*1000
                print("%s : %d ms"%(lb,dt))
                results.append(dst)
                if not bTeaching:
                    pass
                    # predict
                    pred = True
                    if len(results[-1].__out__()) > 0:
                        visualizes.append(dst.visualize(mat=results[0].mat,pprint=pprint,res=True))
                    else:
                        visualizes.append(dst.visualize(mat=results[0].mat,pprint=pprint,res=False))
                        pred = False
                else:
                    visualizes.append(dst.visualize(mat=results[-1].mat,pprint=pprint,res=None))
                    pred = True
                    pass
  
    
    # 

    # visualizes.append(dst.visualize(mat=results[0].mat,pprint=pprint,res=True))
            # except:
            #     print("has a problem at %s"%lb)
    end = time.time()
    dt = (end-start)*1000
    print("time inferenc : %d ms"%(dt))
    # ======================     
    return results,visualizes,pred


if __name__ == "__main__":
    # from collections import Counter

   
    
    # _,mat = cv2.threshold(mat,150,255,0)

    # t = Timer()
    # t.start()
    
    config      = ConfigParser()
    config.read("Model/WebCam-0/para.config")
    config      = config["shape-0"]
    config      = configProxy2dict(config)
   
    mat = cv2.imread("grab/050120_015603.png")
    dst = Mat(mat)
    funcs       = ["Crop","Convert","Binary","Contours","Remove","ConvexHull"]
    for f in funcs:
        dst = DEF_FUNCTIONS[eval(f)](dst,config)
    out = dst.visualize(mat=None,pprint=True)

    # print(DEF_FUNCTIONS)
    # try :
    # print(eval("Crop"))
    # print(DEF_FUNCTIONS[eval("Crop")])
    # for class_,func in DEF_FUNCTIONS.items():
    #     print(class_.__checkin__)
    # except:
    # print("err")


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
    cv2.imshow("",out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
