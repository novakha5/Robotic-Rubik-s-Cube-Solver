import color_detect as detect
import classification_of_color as classify
import refactor as ref
import cv2
import picamera
import serial
import time
import os
from threading import Thread
import socket
import sys

def saveToArr(color, j):
    for i in range(9):
        color_arr[(j*9)+i] = color[i]

color_arr = [(0, 0, 0)for x in range(54)]

#sequence of moves for scanning cube
def scan(i):
    if i == 0:
	string = "E cD "
    elif i == 1:
	string = "cD2 "
    elif i == 2:
	string = "cD e F Ab "
    elif i == 3:
	string = "Ab2 "
    elif i == 4:
	string = "Ab f E Ab e F "
    elif i == 5:
	string = "Ab2 "
    else:
	string = "aB2 f E Ab e "
    return string

def serverFunction():
    
    os.chdir("RubiksCube-TwophaseSolver-master/")
    os.system("python3 run_two_phase_alg.py")


def runCube():
        
	with picamera.PiCamera() as camera:
            camera.start_preview()    
            usart.write(scan(0)) #send first move

            for i in range(6):        
                    #camera.start_preview()
                    read_data = usart.readline() #wait for massage
                    #print(read_data)
                    read_data = read_data.strip()
                    print("in for: {0}").format(read_data)
                    while(read_data != "Done"):
                            if(read_data == "Ready"):
                                    usart.write("R")
                                    camera.stop_preview()
                                    return
                            read_data = usart.readline() #wait for massage 'Done'
                            read_data = read_data.strip()
                            print("in while: {0}").format(read_data)
                    time.sleep(2)
                    #take a picture
                    camera.capture("img.jpg")
                    image = cv2.imread("img.jpg")
                    #camera.stop_preview()
                    #send next move to stm
                    usart.write(scan(i+1))
                    
                    #get colors from picture
                    color = detect.getColorsFromPic(image)
                    saveToArr(color, i)
                    print(color)
            camera.stop_preview()
        
	#classify readed colors
	string = classify.classify(color_arr)
        print(string)	
	#send string of state to Kociemba's algorithm
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 8080)
        sock.connect(server_address)

        try:
            sock.sendall(string)
            data = sock.recv(128)

        finally:
            sock.close()
        
        #print(data)
        #raw_input()

	commands = ref.refactor(data)

        print(commands)
    
	#send solution to stm
	usart.write(commands)

t = Thread(target = serverFunction)
t.setDaemon(True)
t.start()

#starts UART communication
usart = serial.Serial("/dev/ttyAMA0")
usart.baudrate = 9600
usart.write("R")#send ready to stm

#start server for solution 
while(1):
        
	read_data = usart.readline() #wait for massage 
        read_data = read_data.strip()
        #print("nacteno: {0}").format(read_data)
        if(read_data == "Ready"):
		usart.write("R")
	if(read_data == "Start"):
        	runCube()
