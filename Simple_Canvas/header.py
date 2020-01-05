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

# tesseract
# tessdata_dir_config = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR'

