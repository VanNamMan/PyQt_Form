import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk

class myRect:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.tl = [x,y]
        self.br = [w,h]
class myCanvas(tk.Canvas):
    def __init__(self,parent,bg="black",w=300,h=200):
        super(myCanvas,self).__init__(parent,bg=bg,width=w,height=h)
        self.bDrawAlign = False
        self.bDrawRect = False
        self.bDrawLine = False
        self.bActiveRect = False
        self.start = None

        self.photoImg = None
        self.crop = None

        self.rect = [0,0,0,0]
        self.rect_active = [0,0,0,0]
        self.id_rect_active = -1
        self.rects = []
        self.color = "red"
        self.faceColor = "yellow"
        self.font = "Times 14 bold"
        self.lw = 3

        self.bind("<ButtonPress-1>",self.lButtonDown)
        self.bind("<Motion>",self.mouseMove)
        self.bind("<ButtonRelease-1>",self.lButtonUp)

    def lButtonDown(self,e):
        p = [e.x,e.y]
        b,idRect = self.checkPoint(p)
        # for r in self.rects:
        #     if self.ptInRect(p,r):
        #         self.id_rect_active = self.rects.index(r)
        if b:
            self.id_rect_active = idRect
            self.rect_active = self.rects[idRect]
            self.bActiveRect = True
            self.bDrawRect = True
            # self.create_rectangle(r[0],r[1],r[2],r[3]
        if not self.bDrawRect:
            return
        self.bDrawAlign = False
        self.start = e

    def lButtonUp(self,e):
        if not self.bDrawRect:
            return
        self.bDrawAlign = False
        self.bDrawRect = False
        self.bActiveRect = False
        
    def mouseMove(self,e):
        p = [e.x,e.y]
        bCursor = False
        idRect = False

        bCursor,idRect = self.checkPoint(p)
        if bCursor:
            self.configure(cursor="hand2")
            self.reDrawCanvas(self.rects,idRect)
        else:
            self.configure(cursor="plus")

        if not self.bDrawRect:
            return
        if self.bActiveRect:
            dx = e.x - self.start.x
            dy= e.y - self.start.y
            r = self.rect_active
            self.rects[self.id_rect_active] = [r[0]+dx,r[1]+dy,r[2]+dx,r[3]+dy]
            self.reDrawCanvas(self.rects,self.id_rect_active)
            self.crop = self.croped(self.rects[self.id_rect_active])
            pass
        else :
            if self.bDrawAlign:
                self.reDrawCanvas(self.rects,-1)
                self.create_line(0,e.y,self.winfo_width(),e.y
                                    ,fill=self.color,width=self.lw)
                self.create_line(e.x,0,e.x,self.winfo_height()
                                    ,fill=self.color,width=self.lw)
            else:
                self.reDrawCanvas(self.rects,-1)
                if self.start:
                    self.rect = [self.start.x,self.start.y,e.x,e.y]
                    self.create_rectangle(self.start.x,self.start.y,e.x,e.y
                                    ,outline=self.color,width=self.lw)
    def reDrawCanvas(self,rects,idActive):
        self.delete("all")
        if self.photoImg:
                self.showImage(self.photoImg)
        for i in range(len(self.rects)):
            r = self.rects[i]
            if i != idActive:
                color = self.color
            else:
                color = "yellow"
            self.create_rectangle(r[0],r[1],r[2],r[3]
                                    ,outline=color,width=self.lw)
            self.create_text(r[0]-5,r[1]-5,fill=self.faceColor,font=self.font,
                    text="%d"%i)

    def checkPoint(self,p):
        for r in self.rects:
            if self.ptInRect(p,r):
                self.create_rectangle(r[0],r[1],r[2],r[3]
                                    ,outline="yellow",width=self.lw)
                return True,self.rects.index(r)
        return False,-1
    def ptInRect(self,p,r):
        if r[0] < p[0] < r[2] and r[1] < p[1] < r[3]:
            return True
        else:
            return False
        pass
    def resetCanvas(self):
        self.rects = []
        self.reDrawCanvas(self.rects,-1)
    def croped(self,r):
        x1,y1,x2,y2 = r
        wRoot = self.winfo_width()
        hRoot = self.winfo_height()
        x1,y1,x2,y2= [max(x1/wRoot,0),max(y1/hRoot,0),min(x2/wRoot,1),min(y2/hRoot,1)]
        return [x1,y1,x2,y2]
    def showImage(self,photoImg):
        self.photoImg = photoImg
        self.create_image(1,1,anchor="nw",image=photoImg)

            


            





