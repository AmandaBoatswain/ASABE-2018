# -*- coding: utf-8 -*- # 

"""  Created on Wed Jul 18 21:06:07 2018
FILE NAME 
McGill University
ASABE 2016
"""

# Program Properties 
__author__ = "Amanda Boatswain Jacques"
__version__ = 0.1 

# Libraries
import ball_detection
import cv2
import datetime
import numpy as np
import time  
import argparse
import sys
import ast
import json
import os
from datetime import datetime
from serial import Serial, SerialException

"""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, help="Path to the source image")
ap.add_argument("-t", "--template", required=True, help="Path to the template image")
args = vars(ap.parse_args())
"""

### Variable Initialization ###  

class ApplePicker: 
    
    ### Initilaize Robot 
    def __init__(self, source, direction = "right"):        
       
        # Configuration
        try: 
            self.camera = cv2.VideoCapture(source)
            self.pretty_print("[INFO] CAMERA", "Camera initialized!")
            
        except Exception as e:
            self.pretty_print("[ERROR] CAMERA", "Error: %s" % str(e))
            
        self.direction = direction
        
    ### Close
    def close(self):
        self.pretty_print("[INFO] WARN", "Shutdown triggered!")
        sys.exit()
       
    ### Useful Functions ###
    def pretty_print(self, task, msg):    
        """ Pretty Print """ 
        date = datetime.strftime(datetime.now(), '%d/%b/%Y:%H:%M:%S')
        print('[%s] %s\t%s' % (date, task, msg))
        
    ### Camera Functions     
    def capture_image(self, zone=0, write = False, ramp_frames=60):       
        """ Captures a single image from the camera and returns it in PNG format
        read is the easiest way to get a full image out of a VideoCapture object. Will 
        write the photos according to each zone if zone number is provided. """

        self.pretty_print("[INFO] CAMERA", "Capturing photo...")
     
        # Let the camera stabilize for 60 frames 
        for i in range(ramp_frames):
            (retval, self.bgr) = self.camera.read()
                    
        # Save the image 
        if write == True:
            self.filename = "zone_" + str(zone) + ".png"
            cv2.imwrite(self.filename, self.bgr)
            self.pretty_print("[INFO] CAMERA", "Saved image as: " + self.filename)                    
        else:
            pass           
        del(self.camera)
        
        return self.bgr
    
    ### Initialize Arduino
    def init_arduino(self, arduino_dev, arduino_timeout=10, wait=2.0, attempts=3, baud_rate = 9600):
        """ Initialize the connection to the Arduino Board. Need to pass the "COM" port 
        where the Arduino located. """
        
        self.ARDUINO_DEV = arduino_dev
        self.ARDUINO_TIMEOUT = arduino_timeout
        self.ARDUINO_BAUD = baud_rate
        self.pretty_print("[INFO] CTRL", "Initializing Arduino ...")
        
        try:
            self.arduino = Serial(self.ARDUINO_DEV, self.ARDUINO_BAUD, timeout=self.ARDUINO_TIMEOUT )
            self.pretty_print("[INFO] CTRL", "Arduino initialized!")
        except Exception as e:
            self.pretty_print("[ERROR] CTRL", "Error: %s" % str(e))
                 
    ### Execute robotic action
    def execute_action(self, action, attempts=5, wait=2.0):
        # execute an action on the Arduino. """ """
        
        self.pretty_print("[INFO] CTRL", "Interacting with controller ...")
        
        try:
            self.pretty_print("[INFO] CTRL", "Command: %s" % str(action))
            self.arduino.write(str(action)) # send command
            time.sleep(wait)
            status = None
            
            while status == None:
                try:
                    string = self.arduino.readline()
                    status = ast.literal_eval(string) # parse status response
                except SyntaxError as e:
                    self.pretty_print("[ERROR] CTRL", "Error: %s (%s)" % (str(e), string))
                    time.sleep(wait)
                except ValueError as e:
                    self.pretty_print("[ERROR] CTRL", "Error: %s (%s)" % (str(e), string))
                    time.sleep(wait)
            self.pretty_print("CTRL", "Status: %s" % status)
            self.last_action = action
            return status
        
        except Exception as e:
            self.pretty_print("CTRL", "Error: %s" % str(e))
            status = {
                'command' : '?', 
                'result' : 255
            }
            return status             
            
        """
