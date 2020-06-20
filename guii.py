import tkinter
from tkinter import *
from tkinter import ttk
import time
from time import sleep
import numpy as np
import cv2
import datetime as dt
from datetime import datetime
from threading import Thread
from imutils.video import VideoStream
import imutils
import matplotlib
matplotlib.use("TkAgg")
from hello import hel
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
#from scipy.spatial import distance as dist
#from imutils import perspective
#from imutils import contours

#camera initiaization
cap = cv2.VideoCapture(0)
cap.set(32, 640)
cap.set(4, 480)
cap.set(10, 100)

#figure animation
fig = Figure(figsize=(4,3), dpi=80)
ax = fig.add_subplot(111)


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

#start processes
def start():
    pass


#main GUI size
def centre_window(w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) + 0
    y = (hs/2) - 0
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
#capture image and diplay in frame
def capture():
    f = open("images/laser.txt", "w")  # append mode
    f1 = open("images/step.txt", "w")  # append mode
    #frame, img = cap.read()
    path = "images/bamboref.JPG"
    img = cv2.imread(path)
    #cv2.imshow("nil", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([0, 0, 48])
    upper_green = np.array([179, 33, 255])
    green_mask = cv2.inRange(imgHSV, lower_green, upper_green)
    green = cv2.bitwise_and(img, img, mask=green_mask)
    #masking for getting green color seperated
    dimensions = img.shape
    #print(dimensions)
    imheight = dimensions[0]
    imheight = imheight //5
    #print("imheight", imheight)
    imwidth = dimensions[1]
    #print("imwidth", imwidth)
    #cv2.line(green, (488, imheight//4), (536, imheight//4), (0, 255, 0), 3)

    # for x in range (1, imwidth):
    #     for y in range (1, 5):
    #         # see pixel value on masked images and compare change and draw circle
    #         yy=imheight*y
    #         pixel = green[yy, x]
    #         #print(pixel)
    #         #print(pixel[2])
    #         xx = 0
    #         if pixel[1] == xx:
    #             print(x)
    #             f.write("%s \n" % (x))
    #             center_coordinates = (x, yy)
    #             color = (255, 0, 0)
    #             radius = 2
    #             thickness = 1
    #             #print(pixel[1])
    #             #f.write("%s \n" %(x))
    #             f1.write("%s \n" %(yy))
    #             cv2.circle(img, center_coordinates, radius, color, thickness)
    #             #corLable = Label(root, text=center_coordinates).pack(side = LEFT)
    #         #f.write("\n")
    #     #f.write("\n")

    # for x in range (1, imwidth):
    #     # see pixel value on masked images and compare change and draw circle
    #     pixel = green[imheight*2, x]
    #     #print(pixel)
    #     #print(pixel[2])
    #     xx = 0
    #     if pixel[1] == xx:
    #         #print("x", x)
    #         f.write("%s \n" %(x))
    #         center_coordinates = (x, imheight*2)
    #         #print(center_coordinates)
    #         color = (255, 0, 0)
    #         radius = 2
    #         thickness = 1
    #         f1.write("%s \n" %(imheight*2))
    #         cv2.circle(img, center_coordinates, radius, color, thickness)
    #
    # for x in range(1, imwidth):
    #     # see pixel value on masked images and compare change and draw circle
    #     pixel = green[imheight * 3, x]
    #     # print(pixel)
    #     # print(pixel[2])
    #     xx = 0
    #     if pixel[1] == xx:
    #         # print("x", x)
    #         f.write("%s \n" % (x))
    #         center_coordinates = (x, imheight * 3)
    #         # print(center_coordinates)
    #         color = (255, 0, 0)
    #         radius = 2
    #         thickness = 1
    #         f1.write("%s \n" % (imheight * 3))
    #         cv2.circle(img, center_coordinates, radius, color, thickness)
    # y is number of cuts (move stepper vertically) and x is laser on time at that pixle
    for y in range (1, 5):
        for x in range (1, imwidth):
            # see pixel value on masked images and compare change and draw circle
            pixel = green[imheight*y, x]
            #print(pixel)
            #print(pixel[2])
            xx = 0
            if pixel[1] == xx:
                #print("x", x)
                f.write("%s \t" %(x))
                center_coordinates = (x, imheight*y)
                #print(center_coordinates)
                color = (255, 0, 0)
                radius = 2
                thickness = 1
                f1.write("%s \t" %(imheight*y))
                cv2.circle(img, center_coordinates, radius, color, thickness)
        f.write("\n")
        f1.write("\n")
    #this section is to take image divide into 4 sections and generate pixel values corresponding to green color
    #cv2.imshow("grre", green)
    imgStack = stackImages(0.3, ([img, green]))
    cv2.imshow("Image stack", imgStack)
    #cv2.imwrite("images/green.JPG", green, params= None)
    cv2.imwrite("images/imgnew.JPG", imgStack, params= None)
    #print(center_coordinates)
    #corLable = Label(root, text=center_coordinates).pack()

    f.close()
    f1.close()

def cut():
    #fp = "images/coordinate.txt"
    #print(fp)
    df = pd.read_csv('images/laser.txt')
    df1 = pd.read_csv('images/step.txt')
    #Data = pd.read_csv('images/coordinate.txt', usecols = ["cut", "step"])
    #print(cut)
    #df = pd.DataFrame(Data)
    #df.plot(x='cut', y='step',ax=ax)
    #print(df)
    print(df)
    print(df1)
    #canvas = FigureCanvasTkAgg(fig, master=lf)
    #canvas.show()
    #canvas.get_tk_widget().grid(row=0, column=2)
    #root.after(1000, animate())
    #fp.close()


root = Tk()
root.title("Nilesh")
# getting screen's height in pixels
height = root.winfo_screenheight()
# getting screen's width in pixels
width = root.winfo_screenwidth()
#size of GUI on screen size
centre_window(width/2, height/2)


startButton = Button(root, bg="green", text="   Start   ", command=start)
startButton.pack(padx = 10, pady=10, side = LEFT, anchor ='sw')
quitButton = Button(root, bg="red", text="   Quit   ", command=exit)
quitButton.pack(padx = 10, pady=10, side = RIGHT, anchor ='sw')

#label =  ttk.Label(root, text = "Camera")
#frame1 = ttk.LabelFrame(root, height = 640, width = 480, text = "Camera Images" ).pack(padx= 10, pady=10, side = LEFT)
takeImage = Button(root, bg="green", text="   Take   ", command=capture)
takeImage.pack(padx = 10, pady=10, side = LEFT, anchor ='sw')
hellolable= Label(root, text = hel).pack()
cutButton = Button(root, bg="green", text = "Start Cutting", command = cut).pack(padx = 10, pady=10, side = LEFT, anchor ='sw')

lf = ttk.Labelframe(root, text='Past Temp').pack(padx = 10, pady=10, side = LEFT, anchor ='w')

root.mainloop()
