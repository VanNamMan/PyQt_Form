import serial
import serial.tools.list_ports as port_list
import time
import threading
from tkinter import *

def get_decvices():
    list_com = []
    ports = list(port_list.comports())
    for port in ports:
        list_com.append(port.device)
    return list_com

class port():
    def __init__(self,name,baudrate):
        self.name = name
        self.baudrate = baudrate
        self.dataRecieve = ""
        self.serial = self.connect(self.name,self.baudrate)
        
    def connect(self,device_name,baudrate):
        ser = serial.Serial(device_name,baudrate)
        return ser
    def close(self):
        self.serial.close()
        return not self.serial.is_open
    def write(self,data):
        b = bytes(data, 'utf-8')
        self.serial.write(b)
    def read(self,delay):
        while self.serial.is_open: 
            time.sleep(delay)      
            dataRecieve = self.serial.readline(self.serial.in_waiting).decode("utf-8")
            if dataRecieve != "":
                self.dataRecieve = dataRecieve
            if self.dataRecieve != "":
                lb["text"] = (time.strftime("%H:%M:%S : ")+self.dataRecieve)

def loop(ser):
    ser.read(0.001)
    ser.close()

def _ok_():
    print(ser.dataRecieve)

root = Tk()
lb = Label(root,width=20,text="com")
lb.pack()

btn = Button(root,text="OK",command=_ok_).pack()
ser = port("COM9",9600)



thread = threading.Thread(target=loop,args=(ser,))
thread.start()



root.mainloop()



