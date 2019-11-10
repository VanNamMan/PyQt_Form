import cv2
import numpy as np
import pytesseract
from pyzbar import pyzbar
# from pylibdmtx.pylibdmtx import decode as D

# import sklearn.cluster
# from sklearn.externals import joblib

CHECK_TEMPLATE = 0
CHECK_HSV_INRANGE = 1
CHECK_GRAYSCORE = 2
CHECK_AREA = 3


class rect():
    def __init__(self):
        self.x=0
        self.y=0
        self.w=0
        self.h=0
        self.r = [self.x,self.y,self.w,self.h]
    def to_rect(self):
        self.r = [self.x,self.y,self.w,self.h]
    pass 
def getStrDateTime():
        return time.strftime("%d%m%y_%H%M%S")
def toCvRect(frame,image,r):
    if type(image) != type(np.zeros((1,1))):
        return
    W,H = image.shape[1],image.shape[0]
    ratio_x = W/frame.width()
    ratio_y = H/frame.height()
    if len(r) == 4:
        x,y,w,h = r
        X,Y,W,H = int(x*ratio_x),int(y*ratio_y),int(w*ratio_x),int(h*ratio_y)
        return [X,Y,W,H]
    elif len(r) == 2:
        x,y = r
        X,Y = int(x*ratio_x),int(y*ratio_y)
        return [X,Y]
def ptInRect(point,r):
    x,y = point
    if x < r[0]+r[2] and x > r[0] and y < r[1]+r[3] and y > r[1]:
        return True
    else:
        return False
def toRoi(img,roi):
    x,y,w,h = roi
    return img[y:y+h,x:x+w]

def bgr2gray(img):
    if len(img.shape) > 2:
        return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        return img
def gray2bgr(img):
    if len(img.shape) >2:
        return img
    else:
        return cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        

def matching(src,temp,method=cv2.TM_CCOEFF_NORMED,threshold=0.8):
    if len(src.shape) > 2:
        copy = bgr2gray(src)
    else:
        copy = src.copy()
    W,H = copy.shape[::-1]
    w,h = temp.shape[::-1]
    if W<w or H<h:
        return [0,0,0,0],[0,0]
    
    res = cv2.matchTemplate(copy,temp,method=method)
    _,maxVal,_,maxLoc = cv2.minMaxLoc(res)
    return maxVal,maxLoc

"""
--oem
  0    Legacy engine only.
  1    Neural nets LSTM engine only.
  2    Legacy + LSTM engines.
  3    Default, based on what is available.

--psm
  0 = Orientation and script detection (OSD) only.
  1 = Automatic page segmentation with OSD.
  2 = Automatic page segmentation, but no OSD, or OCR
  3 = Fully automatic page segmentation, but no OSD. (Default)
  4 = Assume a single column of text of variable sizes.
  5 = Assume a single uniform block of vertically aligned text.
  6 = Assume a single uniform block of text.
  7 = Treat the image as a single text line.
  8 = Treat the image as a single word.
  9 = Treat the image as a single word in a circle.
  10 = Treat the image as a single character.

"""
def inrange(img,lower,upper):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower = lower
    upper = upper
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv,lower,upper)
    # Bitwise-AND mask and original image
    return mask


def get_text(img,oem=1,psm=7):
    config = ('-l eng --oem %d --psm %d'%(oem,psm))
    try:
        return pytesseract.image_to_string(img,config=config).split("\n")
    except:
        return ""
def get_deskew(gray): # img : bg BLACK, obj WHITE
    thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    
    return angle

def rotated(img,angle):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center,angle, 1.0)
    rot = cv2.warpAffine(img, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rot

def getCode(img):
    code = []
    try:
        code = pyzbar.decode(img)
        return code
    except:
        return None
    pass

def InList(a,lst=(0,10)):
    if lst[1] == -1:
        if lst[0]<a:
            return True
        else:
            return False
    else:
        if lst[0]<a<lst[1]:
            return True
        else:
            return False
def keyX(a):
    x,y,w,h = a
    return x
def keyY(a):
    x,y,w,h = a
    return y
def keyArea(a):
    x,y,w,h = a
    return w*h
def str2ListInt(string):
    lst = string.split(",")
    try:
        A = []
        for l in lst :
            A.append(int(l))
        return A
    except:
        return len(lst)*[0]
    pass
def sub(list1,list2):
    lst = []
    for i in range(len(list1)):
        l1 = list1[i]
        l2 = list2[i]
        lst.append(l2-l1)
    return lst
def add(list1,list2):
    lst = []
    for i in range(len(list1)):
        l1 = list1[i]
        l2 = list2[i]
        lst.append(l1+l2)
    return lst

def str2int(string):
    try:
        return int(string)
    except:
        return 0
def binary(img,k=50,mode=cv2.THRESH_BINARY):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    blur = cv2.GaussianBlur(img,(3,3),0)
    ret,res = cv2.threshold(gray,k,255,mode)
    return res
def removeBlob(binary,area=(0,100),width=(0,20),height=(0,20)):
    A = []
    _,cnts,_ = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if not InList(w,width) or not InList(h,height) or not InList(w*h,area):
            binary[y:y+h,x:x+w] = 0
        else:
            a = [x,y,w,h]
            A.append(a)
    # A.sort(key=keyArea)
    return binary,A
    
def dilate(binary,kSize=5,iters=1):
    try:
        kernel = np.ones((kSize,kSize),np.uint8)
        dilate = cv2.dilate(binary,kernel,iterations=iters)
        return dilate
    except:
        return binary




