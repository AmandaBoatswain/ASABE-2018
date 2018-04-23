# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:39:30 2018
@author: Ryan, Amanda, Trev Stanhope

-- ball_detect_images.py - A script to locate red balls in a video, draw circles 
around them and locate their center points.  
"""

# Libraries
import cv2
import numpy as np
import glob         # library for looping through files
import os 
import imutils

# Green Range 
lower_green = np.array([60,50,50])
upper_green = np.array([90,255,255])

# Blue Range 
lower_blue = np.array([100,50,50])
upper_blue = np.array([130,255,255])

# Lower Red range
Llower_red = np.array([0,50,50]) 
Lupper_red = np.array([5,255,255])

# Upper Red range
Ulower_red = np.array([165,50,50])
Uupper_red = np.array([179,255,255])

RADIUS_MIN = 30 # Tweak these 
RADIUS_MAX = 70 # Tweak these 

directory = "./sample_cv_pictures"

for root, dirs, filenames in os.walk(directory):
    for i, file in enumerate(filenames):
        imgpath = os.path.join(root,file) # Reconstructs the file path using
        # grab an image in the file folder 
        bgr = cv2.imread(imgpath)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        # Blur the image and remove speckle noise 
        blur = cv2.medianBlur(hsv, 9)
        blur = cv2.GaussianBlur(hsv, (11,11), 0)
        
        # Create a mask composed of both red ranges and merge together 
        Lred_mask = cv2.inRange(blur,Llower_red,Lupper_red)
        Ured_mask = cv2.inRange(blur,Ulower_red,Uupper_red)
        red_mask = Lred_mask + Ured_mask
        red_mask = cv2.erode(red_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
        red_mask = cv2.dilate(red_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
        # Show only the red objects in the image 
        red_final = cv2.bitwise_and(bgr, bgr, mask=red_mask)
        
        # Create a mask for the blue range 
        blue_mask = cv2.inRange(blur, lower_blue, upper_blue)
        blue_mask = cv2.erode(blue_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
        blue_mask = cv2.dilate(blue_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
        # Show only the blue objects in the image 
        blue_final = cv2.bitwise_and(bgr, bgr, mask = blue_mask)
        
        
        # Create a mask for the green range 
        green_mask = cv2.inRange(blur, lower_green, upper_green)
        green_mask = cv2.erode(green_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
        green_mask = cv2.dilate(green_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
        # Show only the green objects in the image 
        green_final = cv2.bitwise_and(bgr, bgr, mask = green_mask)
        
        ## Find the Contours
        # Red Contours
        red_contours = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None # initialize the current (x, y) center of the ball
        if len(red_contours) > 0: # only proceed if at least one contour was found
            # Find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and centroid
            for c in red_contours:
                k = cv2.isContourConvex(c)
                approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True), True)
                area = cv2.contourArea(c)
                if ((len(approx) > 8) & (area > 30)):
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    print(radius)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if (radius > RADIUS_MIN) and (radius < RADIUS_MAX): # only proceed if the radius meets a minimum size
                        cv2.circle(bgr, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                        cv2.circle(bgr, center, 5, (255, 255, 255), -1)
                        
        # Blue  Contours
        blue_contours = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None # initialize the current (x, y) center of the ball
        if len(blue_contours) > 0: # only proceed if at least one contour was found
            # Find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and centroid
            for c in blue_contours:
                k = cv2.isContourConvex(c)
                approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True), True)
                area = cv2.contourArea(c)
                if ((len(approx) > 8) & (area > 30)):
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    print(radius)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if (radius > RADIUS_MIN) and (radius < RADIUS_MAX): # only proceed if the radius meets a minimum size
                        cv2.circle(bgr, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                        cv2.circle(bgr, center, 5, (255, 255, 255), -1)
                        
        # Green Contours
        green_contours = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None # initialize the current (x, y) center of the ball
        if len(green_contours) > 0: # only proceed if at least one contour was found
            # Find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and centroid
            for c in green_contours:
                k = cv2.isContourConvex(c)
                approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True), True)
                area = cv2.contourArea(c)
                if ((len(approx) > 8) & (area > 30)):
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    print(radius)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if (radius > RADIUS_MIN) and (radius < RADIUS_MAX): # only proceed if the radius meets a minimum size
                        cv2.circle(bgr, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                        cv2.circle(bgr, center, 5, (255, 255, 255), -1)
        

        
        cv2.imshow("original", bgr)
        cv2.imshow("Red", red_final)
        cv2.imshow("Blue", blue_final)
        cv2.imshow("Green", green_final)
        
        cv2.waitKey(0)
    

cv2.destroyAllWindows()

