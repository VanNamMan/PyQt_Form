import sys
from configparser import ConfigParser

class ConfigWriter():
	def __init__(self,filename):
		self.config = ConfigParser()
		self.filename = filename
		pass

	def addConfig(self,id_box,info_box):
		self.config["%d"%id_box] = info_box
	
	def save(self):
		with open(self.filename,"w") as out:
			self.config.write(out)