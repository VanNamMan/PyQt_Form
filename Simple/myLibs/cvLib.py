import cv2
import numpy as np
from pyzbar import pyzbar

def readCode(image):
	barcodes = pyzbar.decode(image)
	return [{"data":code.data.decode("utf-8") 
			, "rect" : code.rect 
			, "type" : code.type} for code in barcodes]
