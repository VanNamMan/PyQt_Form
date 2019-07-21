import cv2
import numpy as np
import pytesseract
from pyzbar.pyzbar import decode
from pylibdmtx.pylibdmtx import decode as D

from PyQt5.QtGui import QImage,qRgb
import qimage2ndarray


def qImageToCvMat(qImg):
    '''  Converts a QImage into an opencv MAT format  '''
    arr = qimage2ndarray.rgb_view(qImg.convertToFormat(QImage.Format_ARGB32))[...,::-1]
    return arr
def cVMatToQImage(cvMat):
	if len(cvMat.shape) == 3:
		return qimage2ndarray.array2qimage(cvMat)
	else:
		return qimage2ndarray.gray2qimage(cvMat)


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

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'

#Add the following config, if you have tessdata error like: "Error opening data file..."
# Example config: r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"'
# It's important to add double quotes around the dir path.
# tessdata_dir_config = r'--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
# pytesseract.image_to_string(image, lang='chi_sim', config=tessdata_dir_config)

def get_text(img,config = ('-l eng --oem 1 --psm 3')):
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return pytesseract.image_to_string(gray).split("\n")
# barcode
def getMatrixCode(img):
	try:
		codes = D(img)
		return [[code.data.decode("utf-8"),code.type]for code in codes]
	except:
		return None
def getBarcode(img):
	try:
		codes = decode(img)
		return [[code.data.decode("utf-8"),code.type]for code in codes]
	except:
		return None