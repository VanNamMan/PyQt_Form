from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

import cv2,os,time,threading,sys
import pandas as pd
import numpy as np
from configparser import ConfigParser
from argparse import ArgumentParser
import re
import serial
from functools import partial
from qimage2ndarray import *
from pytesseract import pytesseract
import subprocess
import shlex

from scipy import misc
from PIL import ImageQt

DEFAULT_FILL_COLOR = QColor(128, 128, 255, 100)
DEFAULT_SELECT_FILL_COLOR = QColor(128, 255, 0, 100)
DEFAULT_VISIBLE_FILL_COLOR = QColor(0, 128, 255, 100)
DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 255)
DEFAULT_VERTEX_SELECT_FILL_COLOR = QColor(255,0,0, 255)

CURSOR_DEFAULT = Qt.ArrowCursor
CURSOR_POINT = Qt.PointingHandCursor
CURSOR_DRAW = Qt.CrossCursor
CURSOR_DRAW_POLYGON = Qt.SizeAllCursor
CURSOR_MOVE = Qt.ClosedHandCursor
CURSOR_GRAB = Qt.OpenHandCursor

# tesseract
# tessdata_dir_config = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR'

