import colordetect as detect
import classification_of_color as classify
import cv2
import picamera
import serial
import time

def saveToArr(color, j):
    for i in range(9):
        color_arr[(j*9)+i] = color[i]

color_arr = [(0, 0, 0)for x in range(54)]

def scan(i):
    if i == 0:
	string = "e cD "
    elif i == 1:
	string = "cD2 "
    elif i == 2:
	string = "cD E aB "
    elif i == 3:
	string = "aB2 "
    elif i == 4:
	string = "aB F e aB E f "
    elif i == 5:
	string = "aB2 "
    else:
	string = ""
    return string

usart = serial.Serial("/dev/ttyAMA0")
usart.baudrate = 9600
usart.write("R")

read_data = usart.readline() #wait for massage 
while(read_data != "Start"):	
	read_data = usart.readline() #wait for massage "Start"

with picamera.PiCamera() as camera:
    camera.start_preview()    
    usart.write(scan(0)) #send first move

    for i in range(6):        
	read_data = usart.readline() #wait for massage
        print(read_data)
	while(read_data != "Done"):
		if(read_data == "Start"):
			usart.write("R")
			usart.write(scan(0))
			i = 0
			color_arr = [(0, 0, 0)for x in range(54)]
		read_data = usart.readline() #wait for massage 'Done'

	time.sleep(2)	
        camera.capture("img.jpg")
        image = cv2.imread("img.jpg")

	usart.write(scan(i+1)) #send next move
        color = detect.getColorsFromPic(image)
        saveToArr(color, i)
    camera.stop_preview()

    string = classify.classify(color_arr)

print(string)