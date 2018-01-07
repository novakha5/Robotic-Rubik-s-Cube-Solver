import picamera
import time
import cv2
import numpy as np
import math
def getColorsFromPic(im):

        def sort(arr):
            changed = True
            while changed:
                changed = False
                for i in range (9 - 1):
                    if arr[i][1] > arr[i+1][1]:
                        tmp = arr[i]
                        arr[i] = arr[i+1]
                        arr[i+1] = tmp
                        changed = True
            changed = True
            while changed:
                changed = False
                for i in (0,1):
                    if arr[i][0] > arr[i+1][0]:
                        tmp = arr[i]
                        arr[i] = arr[i+1]
                        arr[i+1] = tmp
                        changed = True
            changed = True
            while changed:
                changed = False
                for i in (3,4):
                    if arr[i][0] > arr[i+1][0]:
                        tmp = arr[i]
                        arr[i] = arr[i+1]
                        arr[i+1] = tmp
                        changed = True
            changed = True
            while changed:
                changed = False
                for i in (6,7):
                    if arr[i][0] > arr[i+1][0]:
                        tmp = arr[i]
                        arr[i] = arr[i+1]
                        arr[i+1] = tmp
                        changed = True

            print("sorted: {0}").format(arr)
            return arr
	
	def check(arr):
	   point = (0, 0)

	   left_up = arr[0]
	   right_up = arr[2]
	   left_down = arr[6]
	   right_down = arr[8]
	   
	   min_x = left_up[0] 
	   max_x = right_up[0] 
	   min_y = left_up[1]
	   max_y = left_down[1]
	   
	   if(right_down[0] > max_x):
		max_x = right_down[0]
	   if(left_down[0] < min_x):
		min_x = left_down[0]
	   if(right_up[1] < min_y):
		min_y = right_up[1]
	   if(right_down[1] > max_y):
		max_y = right_down[1]

	   x_dist_r = abs(right_down[0] - right_up[0])
	   x_dist_u = abs(right_up[0] - left_up[0])
	   x_dist_l = abs(left_down[0] - left_up[0])
	   x_dist_d = abs(right_down[0] - left_down[0])

	   y_dist_r = abs(right_down[1] - right_up[1])
	   y_dist_u = abs(right_up[1] - left_up[1])
	   y_dist_l = abs(left_down[1] - left_up[1])
	   y_dist_d = abs(right_down[1] - left_down[1])

	   dist_right = math.sqrt(x_dist_r*x_dist_r + y_dist_r*y_dist_r)  
	   dist_up = math.sqrt(x_dist_u*x_dist_u + y_dist_u*y_dist_u)  
	   dist_left = math.sqrt(x_dist_l*x_dist_l + y_dist_l*y_dist_l)  
	   dist_down = math.sqrt(x_dist_d*x_dist_d + y_dist_d*y_dist_d) 

	   min_dist = dist_right
	   max_dist = dist_right
	   
	   if(dist_left < min_dist):
		min_dist = dist_left
	   if(dist_left > max_dist):
		max_dist = dist_left
	   if(dist_up < min_dist):
		min_dist = dist_up
	   if(dist_up > max_dist):
		max_dist = dist_up
	   if(dist_down > max_dist):
		max_dist = dist_down
	   if(dist_down < min_dist):
		min_dist = dist_down
	   
	   distance = 0
	   if(dist_right != min_dist and dist_right != max_dist):
		distance = distance + dist_right	
	   if(dist_left != min_dist and dist_left != max_dist):
		distance = distance + dist_left	
	   if(dist_up != min_dist and dist_up != max_dist):
		distance = distance + dist_up	
	   if(dist_down != min_dist and dist_down != max_dist):
		distance = distance + dist_down	
	   
	   
	   if(distance < min_dist*min_dist):
		if(dist_down == dist_left and dist_left == dist_right and dist_right == dist_up):
			distance == dist_down*2
		elif(dist_down == dist_up or dist_down == dist_left or dist_down == dist_right):
			distance += dist_down
		elif(dist_up == dist_left or dist_down == dist_right):
			distance += dist_up
		elif(dist_left == dist_right):
			distance += dist_left

	   dist = distance/2.0
	   dist_high = dist + dist/16.0
	   dist_low = dist - dist/16.0
	   print(distance)
	   min_x = min_x - dist/16.0
	   max_x = max_x + dist/16.0
	   min_y = min_y - dist/16.0
	   max_y = max_y + dist/16.0
	   for i in range(9):
		if(arr[i][0] < min_x or arr[i][0] > max_x):
			point = arr[i]
			break
		elif(arr[i][1] < min_y or arr[i][1] > max_y):
			point = arr[i]
			break
	   
	   diagonal_high = dist_high*math.sqrt(2)
	   diagonal_low = dist_low*math.sqrt(2)
	   down_dial = dist_down*math.sqrt(2)
	   up_dial = dist_up*math.sqrt(2)
	   right_dial = dist_right*math.sqrt(2)
	   left_dial = dist_left*math.sqrt(2)

	   if(point == (0, 0)):
		if(down_dial > diagonal_high or down_dial < diagonal_low):
			if(dist_right < dist_low or dist_right > dist_high):
				point = right_down
			elif(dist_left < dist_low or dist_left > dist_high):
				point = left_down
		elif(up_dial > diagonal_high or up_dial < diagonal_low):
			if(dist_right < dist_low or dist_right > dist_high):
				point = right_up
			elif(dist_left < dist_low or dist_left > dist_high):
				point = left_up
		elif(right_dial > diagonal_high or right_dial < diagonal_low):
			if(dist_up < dist_low or dist_up > dist_high):
				point = right_up
			elif(dist_down < dist_low or dist_down > dist_high):
				point = right_down
		elif(left_dial > diagonal_high or left_dial < diagonal_low):
			if(dist_up < dist_low or dist_up > dist_high):
				point = left_up
			elif(dist_down < dist_low or dist_down > dist_high):
				point = left_down
	   
	   return point 

	
	def findPoints(filtr, heigth, widith):
	    arr = [[0 for x in range(2)] for y in range(9)]
	    obr = filtr.copy()		
            for i in range(9):
                most_black = 255
                position = (0, 0)
                for j in range(height):
                    for k in range(widith):
                        pixel = obr[j, k]
                        if pixel < most_black:
                            most_black = pixel
                            position = (k, j)
                arr[i] = position
                cv2.circle(obr, position, 20, 255, -1)
                cv2.circle(obr, position, 1, 220, -1)
            return sort(arr)


	points = [[0 for x in range(2)]for y in range(9)]
	image = im
	small = cv2.resize(image, (0,0), fx=0.15, fy=0.15)
        height, widith, ch = small.shape
        if height < widith:
            tmp = (widith - height)/2
            small = small[0:height, tmp:(widith-tmp)]
        else:
            tmp = (height - widith)/2
            small = small[tmp:(height-tmp), 0:widith]
	

	img_hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
	for x in range(0,len(img_hsv)):	
		for y in range(0,len(img_hsv[x])):
			img_hsv[x][y][2] = 130
	img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

	
        pokus = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        closed = cv2.Laplacian(pokus, cv2.CV_8U)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (22, 22))/float(10)
        filtr = cv2.filter2D(closed, -1, kernel)
       
  
        
	height, widith = filtr.shape
        points = findPoints(filtr, height, widith)
	point = check(points)
	
	while point != (0, 0):	
		cv2.circle(filtr, point, 5, 255, -1)
                cv2.circle(filtr, point, 1, 220, -1) 
        	points = findPoints(filtr, height, widith)
		point = check(points)
		
	
	color = [0 for x in range(9)]
        for i in range(0,9):
            b, g, r = img_bgr[points[i][1], points[i][0]]
            color[i] = (b, g, r)
            b = int(b)
            g = int(g)
            r = int(r)
            position = (points[i][0], points[i][1])
            cv2.circle(img_bgr, position, 3, (0, 0, 0), -1)
	    cv2.circle(img_bgr, position, 2, (b, g, r), -1)

	return color

