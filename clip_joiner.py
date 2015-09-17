# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:43:27 2015

The user can select a working directory where from all mp4s can be compiled
into one large clip and then saved in the same location.

@author: Jason
"""

import numpy as np
from moviepy.editor import *
import os
from moviepy.video.tools.segmenting import findObjects

while(True):
    #Display CWD and ask user to continue or enter a new one
    print ("The current working directory is: %s" % os.getcwd())
    while(True):
        input1 = raw_input("Press ENTER to continue or input another location: ")
        if input1 == '':
            break
        else:
            print("\nYou've selected...")
            #Change working directory to user chosen folder
            os.chdir(input1)
            print(os.getcwd())
            print("\nThe working directory has successfully been changed")
    
    #Read every file in folder and display mp4's to user
    fileList = os.listdir(os.getcwd())
    print("\nThis folder contains:")
    mp4List = []
    for f in fileList:
        if f[-4:] == ".mp4":
            mp4List.append(f)
            print f
    
    #Load clips from list into a list of clips
    clips = [VideoFileClip(n) for n in mp4List]
    
    #Add transparent text of the name for each clip as it plays
    #   To be added
    
    #Append all the clips into one large clip
    comp = concatenate(clips, method="compose")
    comp.fps = 24
    
    #Ask for name of video composition
    comp_name = raw_input("\nEnter a name for the video composition: ")
    
    #Save composition to file
    comp.write_videofile("%s.mp4" % comp_name)
    
    #Ask user to exit or start over
    while(True):
        input1 = raw_input("Would you like to start over?[y]/n: ")
        if input1 == 'y' or input1 == '':
            break
        elif input1 == 'n':
            raise SystemExit
            print("AUTO EXIT FAILED!! Please exit the system!")
        else:
            print("Your input is not valid. Please try again...")
