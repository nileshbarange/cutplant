import time
import datetime
import tkinter as tk
import tkinter.font as tkFont
import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import cv2

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from tkinter import ttk
import matplotlib.animation as animation
from matplotlib import style

# Declare global variables
root = None
dfont = None
frame = None

# Global variable to remember if we are fullscreen or windowed
fullscreen = False
#camera initiaization
cap = cv2.VideoCapture(0)
cap.set(32, 640)
cap.set(4, 480)
cap.set(10, 100)

#figure animation
fig = Figure(figsize=(4,3), dpi=80)
ax = fig.add_subplot(111)
al = np.array([], dtype='int8')
ast = np.array([],dtype='int8')
alll = np.array([],dtype='int8')
astt = np.array([],dtype='int8')
count = None
count1 = None
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
    global al, ast, count1, count, alll, astt
    #print(al)

    # y is number of cuts (move stepper vertically) and x is laser on time at that pixle
    for y in range (1, 5):
        count = 0
        for x in range (1, imwidth):
            # see pixel value on masked images and compare change and draw circle
            n = imheight * y
            #print("n", n)
            pixel = green[n, x]
            #print(pixel)
            #print(pixel[2])
            xx = 0
            if pixel[1] == xx:
                #print("x", x)
                count = count + 1
                f.write("%s \t" %(x))
                al = np.append(al, x)
                #print(al)
                #al.append(x)
                center_coordinates = (x, n)
                #print(center_coordinates)
                color = (255, 0, 0)
                radius = 2
                thickness = 1
                f1.write("%s \t" %(n))
                #ast.append(n)
                ast = np.append(ast, n)
                cv2.circle(img, center_coordinates, radius, color, thickness)
        alll = np.append(alll, count)
        #print(alll)
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
    print("Number of cut pixel positions", alll)
    y1 = alll[0]
    y2 = alll[1]
    y3 = alll[2]
    y4 = alll[3]
    #ycutLable = Label(root, text="Y Cut @ ").pack(side = LEFT, anchor ='w')
    #listbox1 = Listbox(root)
    #listbox1.pack(side = LEFT)
    print(y1,y2,y3,y4)
    #print("al pixel",al)
    fal = open("images/al.txt", "w")  # append mode
    #fast = open("images/ast.txt", "w")  # append mode
    print("1st pixel")
    #corLable4 = Label(root, text=ast[0]).pack(side = LEFT, anchor ='w')
    for i in range(0,68):
        fal.write("%s \t" % (al[i]))
        #corLable = Label(root, text=al[i]).pack()
        #listbox1.insert(END, al[i])
        print(al[i])
    fal.write("\n")

    print("2nd pixel")
    y22 = y1+y2
    #corLable1 = Label(root, text=ast[y1 + 1]).pack(side = LEFT, anchor ='w')
    for i in range(y1,y22):
        print(al[i])
        fal.write("%s \t" % (al[i]))
    fal.write("\n")
    print("3rd pixel")
    y33 = y1+y2+y3
   # corLable2 = Label(root, text=ast[y1 + y2 + 1]).pack(side = LEFT, anchor ='w')
    for i in range(y1+y2,y33):
        print(al[i])
        fal.write("%s \t" % (al[i]))
    fal.write("\n")
    print("4th pixel")
    y44 = y1+y2+y3+y4
    #corLable3 = Label(root, text=ast[y1 + y2 + y3 + 1]).pack(side = LEFT, anchor ='w')
    for i in range(y1+y2+y3,y44):
        #print(y3+1, y4)
        fal.write("%s \t" % (al[i]))
        print(al[i])
    fal.write("\n")

    print("y move     ")
    print(ast[0])
    print(ast[y1+1])
    print(ast[y1+y2+1])
    print(ast[y1+y2+y3+1])
    fal.close()

# Toggle fullscreen
def toggle_fullscreen(event=None):
    global root
    global fullscreen
    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize()


# Return to windowed mode
def end_fullscreen(event=None):
    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = True
    root.attributes('-fullscreen', False)
    resize()


# Automatically resize font size based on window size
def resize(event=None):
    global dfont
    global frame
    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 20)))
    dfont.configure(size=new_size)



#start processes
def start():
    print("Start")


# Read values from the sensors at regular intervals
def poll():
    global root
    pass

# Main script

# Create the main window
root = tk.Tk()
root.title("The Big Screen")

frame = tk.Frame(root)

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# Create dynamic font for text
dfont = tkFont.Font(size=1)

# Create widgets
label_temp = tk.Label(frame, text="Nilesh's ", font=dfont)
button_quit = tk.Button(frame, text="Quit", font=dfont, command=root.destroy)
button_start = tk.Button(frame, text="Start", font=dfont, command=start)
button_take= tk.Button(frame, text="Take", font=dfont, command=capture)
button_cut= tk.Button(frame, text="Cut", font=dfont, command=cut)

# Lay out widgets in a grid in the frame
label_temp.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
button_quit.grid(row=2, column=2, padx=5, pady=5)
button_start.grid(row=1, column=0, padx=5, pady=5)
button_take.grid(row=2, column=0, padx=5, pady=5)
button_cut.grid(row=3, column=1, padx=5, pady=5)


# Make it so that the grid cells expand out to fill window
for i in range(0, 3):
    frame.rowconfigure(i, weight=1)
for i in range(0, 3):
    frame.columnconfigure(i, weight=1)
# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)
# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)
# Schedule the poll() function to be called periodically
root.after(500, poll)

# Start in fullscreen mode and run
toggle_fullscreen()
root.mainloop()


