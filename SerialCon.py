from tkinter import *
from tkinter import messagebox
import serial,os,sys
from time import sleep,time
from threading import Thread
import serial.tools.list_ports as port_list
import re
def getcoms():
    _ports_ = list(port_list.comports())
    ports = []
    for p in _ports_:
        ports.append(re.findall("COM.",str(p))[0])
    return ports
def bsleep(seconds_to_sleep):
    start = time()
    while (time() < start + seconds_to_sleep):
        pass
    
class Serialcon:
  def __init__(self):
     self.window=Tk()
     self.window.title("SerialCon")
     self.window.geometry("500x500")
     self.window.resizable(False, False)
     datafile = "logo2.ico" 
     self.window.iconbitmap("logo2.ico")
     self.window.configure(bg='black')
     self.cv = StringVar()
     com="COM notfound"
     startcom=getcoms()
     if len(startcom)==1:
        com=startcom[0]
     self.cv.set(com)
     self.bv = StringVar()
     self.bv.set("baudrate 115200")
     self.bm=OptionMenu(self.window,self.bv,"baudrate 4800","baudrate 9600","baudrate 19200","baudrate 57600","baudrate 115200")
     self.bm.config(bg = "gray",activebackground="gray",fg="yellow",highlightthickness=0) 
     self.ui=Entry(self.window,width=29,font="Helvetica 20 bold",bg="gray",fg="yellow")
     self.sm = Text(self.window,height=22,width=68,font="Helvetica 10 bold",bg="gray",fg="white")
     self.cbv = StringVar()
     self.cbv.set("waiting")
     self.cb=Label(self.window,textvariable=self.cbv,bg = "black",activebackground="gray",fg="yellow",highlightthickness=0,font="Helvetica 15 bold")
     self.i=0
     self.run=True
     self.rbv=True
     self.vcrun=True
     self.mainpage()
  def otocom(self,coms):
     startcom=coms
     if len(startcom)==1:
        com=startcom[0]
        self.cv.set(com)

  def con(self,cv,bv,t=False):
     if t==True:
        if self.co():
           return self.serial
     
     try:
      ser = serial.Serial(
      port=cv,
      baudrate=int(bv),
      parity=serial.PARITY_ODD,
      stopbits=serial.STOPBITS_TWO,
      bytesize=serial.SEVENBITS
      )
      return ser
     except:
      self.cbv.set("waiting for connection.  ")
      sleep(0.3)
      self.cbv.set("waiting for connection.. ")
      sleep(0.3)
      self.cbv.set("waiting for connection...")
      sleep(0.3)
      return False
  def vc(self):
     while self.vcrun:
      sleep(1)
      coms=getcoms()
      if coms:
         self.otocom(coms)
         self.cm=OptionMenu(self.window,self.cv,*coms)
      else:
         self.cm=OptionMenu(self.window,self.cv,"usb yi tak","usb in bozuk olabilir","hiç açık comport yok")
      self.cm.config(bg = "gray",activebackground="gray",fg="yellow",highlightthickness=0)
      self.cm.place(x=0,y=0)
      baudrate=self.bv.get().replace("baudrate ","")
      com=self.cv.get().replace(" ","")
      try:
        if self.baudrate!=baudrate or self.com!=com:
           self.com=com
           self.baudrate=baudrate
           self.sm.delete('1.0', END)
           self.run=False
           self.run=True
           self.serial.close()
           self.serial=False 
      except:
         self.com=com
         self.baudrate=baudrate

  def otocon(self):
     while self.run:
      try:
        self.serial=self.con(self.com,self.baudrate,True)
        if self.serial:
          self.cbv.set("connected.                     ")
          sleep(1)
      except:
         pass     
    
  def co(self):
      try:
        if self.serial.isOpen():
           return  self.serial
      except:
         return False

  def read(self):
      out=""
      while self.rbv:
           try:
            if self.serial:
             try:
              out += self.serial.read().decode("utf-8")
              if out:
                self.sm.delete('1.0', END)
                self.sm.insert("1.0",out)
               
                bsleep(0.012)
             except:
              self.sm.delete('1.0', END)
              out=""
              self.run=False
              self.run=True
              self.serial.close()
              self.serial=False 
           except:
              pass
  def on_closing(self):
    if messagebox.askokcancel("çıkış", "gerçekten çıkmak mı istiyorsun ?"):
        self.vcrun=False
        self.rbv=False
        self.run=False
        self.window.destroy()
  def write(self,event=0):
      val=self.ui.get().encode()
      self.serial.write(val)
      self.serial.write('\n'.encode())
      self.ui.delete(0, END)
      
      
  def mainpage(self):
     title = StringVar()
     title.set("SerialCon")
     dt= Label(self.window, textvariable=title,font="Helvetica 20 bold",bg="black",fg="yellow") 
     dt.place(x = 180,y = 0)
     
     self.bm.place(x=400,y=0)
    
     self.ui.bind('<Return>',self.write)
     self.ui.place(x = 8,y = 50)
     
     b1 = Button(self.window,text="gönder",height = 2,bg="gray",fg="yellow",activebackground="gray",command=self.write)
     b1.place(x = 450,y = 50)
    
     
     self.sm.place(x = 8,y = 100)

     con=Thread(target=self.otocon)
     con.start()
     vc=Thread(target=self.vc)
     vc.start()
     
     r=Thread(target=self.read)
     r.start()
     self.cb.place(x=8,y=460)
     self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
     self.window.mainloop()

w=Serialcon()
