from tkinter import ttk
import tkinter
from tkinter import *
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import pyscreenshot as ImageGrab
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import tensorflow as tf
from test_tf import ocr_handle


root = Tk()
root.title("麻將辨識")

path = StringVar()
file_entry = Entry(root, state='readonly', text=path)

#二值化

def black( f ):
    g = f.copy( )
    nr, nc = f.shape[:2]
    for x in range( nr ):
        for y in range( nc ):
            if(f[x,y]<190):g[x,y] = 0
    return g

def choosepic():
    name = '1'
    img_path = 'D:/screenshot_data/'
    img_type = '.jpg'
    screenshot_path = img_path + name + img_type
    screenshot_img = ImageGrab.grab()
    screenshot_img.save(screenshot_path)
    
    screenshot_img1 = cv2.imread(screenshot_path, 0)
    img1 = black(screenshot_img1)
    img2 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    contours, hierarchy = cv2.findContours( img1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    j=1
    for cont in contours:
        if (cv2.contourArea(cont) < 20000)and(cv2.contourArea(cont) > 9000):
            if(cv2.arcLength(cont, True)<700)and(cv2.arcLength(cont, True)>300):
                x, y, w, h = cv2.boundingRect(cont)
                ROI = screenshot_img1[ y : y + h, x : x + w ]
                ROI2 = cv2.resize(ROI,(28,28))
                cv2.imwrite( "D:/python_opencv/pic/images/%d.jpg" % j, ROI2 )
                j=j+1

def btn():


    a = []
    
    for i in os.listdir('D:/python_opencv/pic/images'):
        print(i)
        path = 'D:/python_opencv/pic/images/'+str(i)
        images2 = cv2.imread(path, 0)
        x = np.array(images2)
        x = np.expand_dims(x, axis=0)
        a.append(x)
        print('loading no.%s image'%i)

    x = np.concatenate([x for x in a])
    
    
    res = ocr_handle(x)
    print(res)
    
    tkinter.messagebox.showinfo('提示', '辨識结果是：%s'%res)
        

mainframe = ttk.Frame(root, padding="5 4 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Button(mainframe, text="截圖", command=choosepic).grid(column=2, row=4, sticky=W)
ttk.Button(mainframe, text="CNN辨識", command=btn).grid(column=4, row=4, sticky=W)

#image_label = ttk.Label(root,compound=CENTER)
#image_label.grid(column=0,row=5, sticky=W)
#bg = "./brid.png"
#pil_image = Image.open(bg)
#pil_image = pil_image.resize((360, 270))
#img = ImageTk.PhotoImage(pil_image)
#image_label.configure(image=img)

root.mainloop()

