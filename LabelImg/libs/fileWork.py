import pandas as pd
import json
import numpy as np
import os

def save_to_csv(filename,data,columns):
    dct = {}
    for i in range(len(columns)):
        dct[columns[i]] = data[:,i]
    df = pd.DataFrame(dct,columns=columns)
    # df.to_csv(filename)
    try:
        if not os.path.isfile(filename):
            df.to_csv(filename,header="column_names",index=False,sep=",")
        else: # else it exists so append without writing the header
            df.to_csv(filename, mode='a',header=False,index=False,sep=",")
        return True
    except:
        return False

# a = np.array([[0,None,"[1]"],[0,None,"[1]"]])
# cols = ["i","x","y"]
# save_to_csv("data.csv",a, cols)
