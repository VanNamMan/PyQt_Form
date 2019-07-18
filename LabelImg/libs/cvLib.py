import cv2
import numpy as np

class Point:
	def __init__(self,x=0,y=0):
		self.x = x
		self.y = y
	def __str__(self):
		return "[{0},{1}]".format(self.x,self.y)
	def __add__(self,other):
		return Point(self.x+other.x,self.y+other.y)
	def __mul__(self,k):
		return Point(k*self.x,k*self.y)
class Rect:
	def __init__(self,x1=0,y1=0,x2=0,y2=0):
		self.tl = Point(x1,y1)
		self.br = Point(x2,y2)
		self.width = x2-x1
		self.height = y2-y1
	def __str__(self):
		return "[{0},{1},{2},{3}]".format(self.tl.x,self.tl.y,self.br.x,self.br.y)
	def __add__(self,other):
		return Rect(self.tl.x+other.x,self.tl.y+other.y,self.br.x+other.x,self.br.y+other.y)
class Color:
	def __init__(self):
		self.green = (0,255,0)
		self.blue = (255,0,0)
		self.red = (0,0,255)
		self.yellow = (0,255,255)
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.lightGray = (224,224,224)
		self.gray = (128,128,128)
		self.darkGray = (64,64,64)
		self.pink = (255,96,208)
		self.purple = (160,32,255)
		self.lightBlue = (80,208,255)
		self.lightGreen = (96,255,128)
		self.orange = (255,160,16)
		self.brown = (160,128,96)
		self.palePink = (255,208,160)	
def bgr2gray(bgr):
	return cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
def rgb2gray(rgb):
	return cv2.cvtColor(bgr,cv2.COLOR_RGB2GRAY)
def gray2bgr(gray):
	return cv2.cvtColor(bgr,cv2.COLOR_GRAY2BGR)
def gray2rgb(gray):
	return cv2.cvtColor(bgr,cv2.COLOR_GRAY2RGB)
def invert(img):
	return 255-img
def get_meanStd(img,rois=-1):
	if rois == -1:
		return cv2.meanStdDev(img)
	else:
		return [cv2.meanStdDev(img[y1:y2,x1:x2]) for x1,y1,x2,y2 in rois]
