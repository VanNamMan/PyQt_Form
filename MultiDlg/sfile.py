import pandas as pd
import xml.etree.ElementTree as ET
import os,time,json

def read_csv(filename,sep=","):
    return pd.read_csv(filename,sep=sep).values
def to_csv(filename,data,colmuns,sep=",",index=False):
    raw_data = {}
    LEN_DATA = len(data)
    LEN_COLS = len(colmuns)
    if LEN_DATA < LEN_COLS:
        data = data + (LEN_COLS - LEN_DATA)*["N"]
    else:
        data = data[:LEN_COLS]
    for i in range(len(colmuns)):
        raw_data[colmuns[i]] = data[i]
    df = pd.DataFrame(raw_data,columns=colmuns)
    try:
        if not os.path.isfile(filename):
            df.to_csv(filename,header="column_names",index=index,sep=sep)
        else: 
            df.to_csv(filename, mode='a',header=False,index=index,sep=sep)
        return True
    except:
            return False
def to_json(filename,dict_data):
    file_json = open(filename,"w")
    try:
        json.dump(dict_data,file_json)
        return True
    except:
        return False
def load_json(filename):
    file_json = open(filename,"r")
    return json.load(file_json)

class xmlFile():
    def __init__(self,filename,mode="w"):
        self.mode = "w"
        self.filename = filename
        if mode == "w":
            if not os.path.exists(self.filename):
                open(filename,"w")
        
        pass
    def createTree(self,name_tree):
        root = ET.Element(name_tree)
        tree = ET.ElementTree(root)
        self.tree = tree
        self.root = root
        return root,tree
    def insertNode(self,tree,name_node):
        return ET.SubElement(tree,name_node)
    def setValue(self,node,value={}):
        items = list(value.items())
        for item in items :
            key,val = item
            node.set(key,val)
    def getValue(self,node):
        return node.attrib
    def getNode(self,node,tag):
        return node.find(tag)
    def save(self,tree):
        tree.write(self.filename)
        pass
    def load(self):
        if self.mode == "r":
            if not os.path.exists(self.filename):
                return False,None
            else:
                root = ET.parse(self.filename)
                return root

        pass


# data = {"a":1,"b":{"c":0,"d":"hello"}}

# to_json("log\\data.json",data)

# data = load_json("log\\data.json")
# print(data)

# columns = ["ModuleId","Rx","Ry","Rz","Shift X","Shift Y","Range","Mark Err","Avg Err","DLL Version"]
# data = [[] for i in range(len(columns))]
# date = time.strftime("%d%m%y")
# log_file = "log\\%s\\data.csv"%date
# if not os.path.exists("log\\%s"%date):
#     os.mkdir("log\\%s"%date)
# to_csv(log_file,data,columns)



