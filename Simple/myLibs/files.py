import pandas as pd
import numpy as np
import configparser 

def save_config(filename,config):
	with open(filename,"w") as myFile:
		config.write(myFile)

def load_config(filename):
	config = configparser.ConfigParser()
	return config.read(filename)