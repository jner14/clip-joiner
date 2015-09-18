# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 18:43:27 2015

The user can select a working directory where from all mp4s can be compiled
into one large clip and then saved in the same location.

Potencial Changes:
- Ask user to set the length of removal from videos' names instead of hard coded to 8
- Remove file type based off last dot not based off -4 index position

@author: Jason
"""

from moviepy.editor import *
import os


def main():
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
        
        #Load first clip to extract screensize
        screensize = VideoFileClip(mp4List[0]).size
        
        #Create text clip array based on the mp4List
        cvcs = []
        for f in mp4List:
            txtClip = TextClip(f[8:-4],color='white', font="Amiri-Bold", fontsize=30)
            cvcs.append(CompositeVideoClip( [txtClip.set_pos('center')], size=screensize).subclip(0,5))
        
        #Load clips from mp4List
        finishedClips = []
        for i in range(len(mp4List)):
            clip = VideoFileClip(mp4List[i])
        
            #Add text clip to each video clip
            finishedClips.append(CompositeVideoClip([clip,cvcs[i]],size=screensize))
            
            #trying to get rid of "too many open files" error
            clip = None
        
        #Append all the clips into one large clip
        comp = concatenate(finishedClips, method="compose")
        comp.fps = 24
        
        #Ask for name of video composition
        comp_name = raw_input("\nEnter a name for the video composition: ")
        
        #Save composition to file
        comp.write_videofile("%s.mp4" % comp_name)
        
        #Clean up
        comp = None
        finishedClips = None
        
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
###End MAIN                

    
main()