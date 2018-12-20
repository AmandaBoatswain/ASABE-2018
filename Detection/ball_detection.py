# -*- coding: utf-8 -*-

"""  Created on Wed Jul 18 21:06:07 2018 

ball_detection.py
McGill University
ASABE 2016
"""

# Program Properties 
__author__ = "Amanda Boatswain Jacques"
__version__ = 0.1 


# Libraries
import cv2
import numpy as np  
from nms import non_max_suppression_fast
import pandas as pd

### Computer Vision ###
def find_balls(bgr, RADIUS_MIN=40, RADIUS_MAX=75):
    """
    Find the contours for all three masks, then use these
    to compute the minimum enclosing circle and centroid
    Returns:
        color : red, blue, green
        pos: x, y, radius (x-y pixel coordinates)
    """
    
    # Green Range 
    lower_green = np.array([60,50,50])
    upper_green = np.array([90,255,255])
    
    # Blue Range 
    lower_blue = np.array([100,50,50])
    upper_blue = np.array([130,255,255])
    
    # Lower Red range
    Llower_red = np.array([0,50,50]) 
    Lupper_red = np.array([20, 255,255])
    
    # Upper Red range
    Ulower_red = np.array([145,50,50])
    Uupper_red = np.array([179,255,255])
        
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # Blur the image and remove speckle noise 
    blur = cv2.medianBlur(hsv, 9)
    blur = cv2.GaussianBlur(hsv, (11,11), 0)
    
    # Create a mask composed of both red ranges and merge together 
    Lred_mask = cv2.inRange(blur,Llower_red,Lupper_red)
    Ured_mask = cv2.inRange(blur,Ulower_red,Uupper_red)
    red_mask = Lred_mask + Ured_mask
    red_mask = cv2.erode(red_mask, np.ones((5, 5), dtype = "uint8"), iterations = 3)
    red_mask = cv2.dilate(red_mask, np.ones((5, 5), dtype = "uint8"), iterations = 3)
    # Show only the red objects in the image 
    red_circles = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, 4.0, 10)
    
    # Create a mask for the blue range 
    blue_mask = cv2.inRange(blur, lower_blue, upper_blue)
    blue_mask = cv2.erode(blue_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
    blue_mask = cv2.dilate(blue_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
    # Show only the blue objects in the image 
    #blue_final = cv2.bitwise_and(bgr, bgr, mask = blue_mask)
    blue_circles = cv2.HoughCircles(blue_mask, cv2.HOUGH_GRADIENT, 4.0, 10)
    
    # Create a mask for the green range 
    green_mask = cv2.inRange(blur, lower_green, upper_green)
    green_mask = cv2.erode(green_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
    green_mask = cv2.dilate(green_mask, np.ones((5,5), dtype = "uint8"), iterations = 3)
    # Show only the green objects in the image 
    #green_final = cv2.bitwise_and(bgr, bgr, mask = green_mask)
    green_circles = cv2.HoughCircles(green_mask, cv2.HOUGH_GRADIENT, 4.0, 10)
        
    if red_circles is not None: 
        red_circles = np.round(red_circles[0, :]).astype("int")
    if blue_circles is not None: 
        blue_circles = np.round(blue_circles[0, :]).astype("int")
    if green_circles is not None: 
        green_circles = np.round(green_circles[0, :]).astype("int")
    
    detected_red_balls = []
    detected_blue_balls = []
    detected_green_balls = []
    
    balls = {}
   
    ### Find the Contours
    # Red Contours
    red_contours = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(red_contours) > 0: # only proceed if at least one contour was found
        # Find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and centroid
        for c in red_contours:
            approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True), True)
            area = cv2.contourArea(c)
            if ((len(approx) > 8) & (area > 30)): # adjust this to make largest 
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                
                #print("red radius :", radius)
                if (radius > RADIUS_MIN) and (radius < RADIUS_MAX): # only proceed 
                    # if the radius meets a minimum size
                    if red_circles is not None:
                        for (x2,y2,r2) in red_circles:
                                d = np.sqrt((x - x2)**2 + (y - y2)**2) # compute 
                                #print(d)
                                # distance between hough circles & minEnclo
                                if d < 20 and (r2 > RADIUS_MIN) and (r2 < RADIUS_MAX):
                                    detected_red_balls.append((x, y, radius))
                                
    # Blue  Contours
    blue_contours = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(blue_contours) > 0: # only proceed if at least one contour was found
        # Find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and centroid
        for c in blue_contours:
            approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True), True)
            area = cv2.contourArea(c)
            if ((len(approx) > 8) & (area > 30)):
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                if (radius > RADIUS_MIN) and (radius < RADIUS_MAX): # only proceed if the radius 
                    # meets a minimum size
                   
                    if blue_circles is not None:
                        for (x2,y2,r2) in blue_circles:
                            d = np.sqrt((x - x2)**2 + (y - y2)**2) # compute 
                            # distance between hough circles & minEnclo
                            if d < 20 and (r2 > RADIUS_MIN) and (r2 < RADIUS_MAX):
                                detected_blue_balls.append((x, y, radius))
                                                                  
    # Green Contours
    green_contours = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(green_contours) > 0: # only proceed if at least one contour was found
        # Find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and centroid
        for c in green_contours:
            approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True), True)
            area = cv2.contourArea(c)
            if ((len(approx) > 8) & (area > 30)):
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                #print("green radius :", radius)
                if green_circles is not None:
                    if (radius > RADIUS_MIN) and (radius < RADIUS_MAX): # only proceed if the radius 
                        # meets a minimum size
                        for (x2, y2, r2) in green_circles:
                            d = np.sqrt((x - x2)**2 + (y - y2)**2)
                            if (d < 20) and (r2 > RADIUS_MIN) and (r2 < RADIUS_MAX):
                                detected_green_balls.append((x, y, radius))
                                
    # Apply Non-Maximum Suppression to the 3 sets, removes duplicate balls in
    # the image that have an overlap percentage of more than 0.5 
    detected_red_balls = np.array(detected_red_balls)
    detected_blue_balls = np.array(detected_blue_balls)
    detected_green_balls = np.array(detected_green_balls)
    
    red_balls = np.array(non_max_suppression_fast(detected_red_balls, 0.5))
    blue_balls = np.array(non_max_suppression_fast(detected_blue_balls, 0.5))
    green_balls = np.array(non_max_suppression_fast(detected_green_balls, 0.5))

    # add a variable for color type
    
    for array in [red_balls, blue_balls, green_balls]:
        if not array.any():
            array = np.empty(array.shape)
            array[:] = np.nan 
    
    balls = {"red": red_balls, "blue": blue_balls, "green": green_balls}
    #df = pd.DataFrame(columns = ["x", "y", "r", "c", "pos"], index = indexes)
    columns = ["x", "y", "r", "c", "pos"]
    df = pd.DataFrame(columns = columns) # initialize the empty DataFrame  
        
    for key in balls.keys():
        found_balls = balls[key]
        if found_balls is not None: 
            print("[INFO] %.i %s balls detected." % (len(found_balls), key))
            for ball in found_balls: 
                x, y, r = np.hsplit(ball, 3)
                
                # Check position of ball
                if y > bgr.shape[0]//2:
                    pos = "B"
                else:
                    pos = "T"
                    
                c = key[0]
                z = pd.DataFrame([[x, y, r, c.upper(), pos]], columns = columns)                
                df = df.append(z, ignore_index = True)
        
            # draw the balls
            for x, y, r in list(found_balls):
                cv2.circle(bgr, (int(x), int(y)), int(r), (0,255,255), 2)
                cv2.circle(bgr, (int(x),int(y)), 3, (255, 255, 255), -1)
                
            cv2.line(bgr, (0, bgr.shape[0]//2),(bgr.shape[1],bgr.shape[0]//2),(0, 255, 255),5)
            
        else:
            # switch to pretty print 
            print("[INFO] No Balls Found!")
            
    return df, bgr


def sort_balls(balls, direction = "left"):
    """
    With dataframe of balls, sort them according to left or right 
    depending on camera direction. 
    """
    
    if direction == "left":
        sorted_balls = balls.sort_values(by = "x", axis = 0, ascending = True)
    if direction == "right":
        sorted_balls = balls.sort_values(by = "x", axis = 0, ascending = False)
    return sorted_balls
      
def create_collection_list(sorted_balls):
    """
    creates a list of all the balls to collect in the appropriate order. This will
    depend on the orientation and setup of the robot.
    """
    collection_list = []
    
    for i, color in enumerate(list(sorted_balls["c"])):
        loc = list(sorted_balls["pos"])[i]
        ball_string = color + loc
        collection_list.append(ball_string) 
        
    return collection_list
    

# For testing purposes  


"""
cap = cv2.VideoCapture(0) # Select the Video Capture Source
 
while(True):
    _, img = cap.read() # Transform the frame into a BGR matrix
    pic_balls, bgr = find_balls(img)
    print("pic balls", pic_balls)
    
    sorted_balls = sort_balls(pic_balls, direction = "right")
    print("sorted_balls", sorted_balls)
    
    
    cv2.imshow("Detected Balls", bgr)
   # To break out of the loop press the "q" key.
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break
    
cap.release()  
cv2.destroyAllWindows()

"""
        
#img = cv2.imread("C:/Users/amand/Documents/Robotics/ASABE 2018 Competition/WIN_20180423_14_55_19_Pro.jpg")
img = cv2.imread("C:/Users/amand/Documents/Robotics/ASABE 2018 Competition/Code/sample_cv_pictures/ball_test4.jpg")
pic_balls, bgr = find_balls(img)


print(pic_balls)
print("original dataframe")
sorted_balls = sort_balls(pic_balls, direction = "left")

print("sorted dataframe")
print(sorted_balls)

ball_list = create_collection_list(sorted_balls)
print(ball_list)


cv2.imshow("Detected Balls", bgr)
cv2.waitKey(0)
cv2.destroyAllWindows() 

