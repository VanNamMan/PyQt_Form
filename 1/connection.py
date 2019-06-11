import serial

class Port:
    def __init__(self,comport,baud):
        self.ser = serial.Serial(comport,baud)
        pass
    def write_(self,data):
        b = bytes(data,"utf-8")
        self.ser.write(b)
    def read_(self):
        data = ""
        try:
            data = self.ser.readline(self.ser.in_waiting).decode("utf-8")
        except:
            data = ""
        return data

# port = Port(comport="COM10",baud=9600)
# b = port.ser.is_open
# while b :
#     data = port.read_()
#     if data != "":
#         print(data)
#     if data == "q":
#         break
# port.ser.close()

