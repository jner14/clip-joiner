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
        txtClipsPlain = []
        cvcs = []
        for f in mp4List:
            txtClipsPlain.append(TextClip(f[:-4],color='white', font="Amiri-Bold",
                               kerning = 5, fontsize=100))
            cvcs.append(CompositeVideoClip( [txtClip.set_pos('center')],
                                     size=screensize, transparent=True))
                                     
        # WE USE THE PLUGIN findObjects TO LOCATE AND SEPARATE EACH LETTER
        letters = [findObjects(cvc) for cvc in cvcs]
#        for cvc in cvcs:
#            letters.append(findObjects(cvc)) # a list of ImageClips
        
        style = [vortex, cascade, arrive, vortexout][random.randint(0,3)]
        txtClipsFancy = [ CompositeVideoClip( moveLetters(l,style),
                          size = screensize).subclip(0,5)
                          for l in letters]
        
        #Load clips from list into a list of clips
        clips = [VideoFileClip(n) for n in mp4List]
        
        #Add fancy text clip to each video clip
        finishedClips = []
        for i in len(clips):
            finishedClips.append(concatenate([clips[i],txtClipsFancy[i]], method="compose"))
        
        #Append all the clips into one large clip
        comp = concatenate(finishedClips, method="compose")
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
###End MAIN                


# helper function
rotMatrix = lambda a: np.array( [[np.cos(a),np.sin(a)], 
                                 [-np.sin(a),np.cos(a)]] )

# THE NEXT FOUR FUNCTIONS DEFINE FOUR WAYS OF MOVING THE LETTERS
def vortex(screenpos,i,nletters):
    d = lambda t : 1.0/(0.3+t**8) #damping
    a = i*np.pi/ nletters # angle of the movement
    v = rotMatrix(a).dot([-1,0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos+400*d(t)*rotMatrix(0.5*d(t)*a).dot(v)
    
def cascade(screenpos,i,nletters):
    v = np.array([0,-1])
    d = lambda t : 1 if t<0 else abs(np.sinc(t)/(1+t**4))
    return lambda t: screenpos+v*400*d(t-0.15*i)

def arrive(screenpos,i,nletters):
    v = np.array([-1,0])
    d = lambda t : max(0, 3-3*t)
    return lambda t: screenpos-400*v*d(t-0.2*i)
    
def vortexout(screenpos,i,nletters):
    d = lambda t : max(0,t) #damping
    a = i*np.pi/ nletters # angle of the movement
    v = rotMatrix(a).dot([-1,0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos+400*d(t-0.1*i)*rotMatrix(-0.2*d(t)*a).dot(v)

# WE ANIMATE THE LETTERS
def moveLetters(letters, funcpos):
    return [ letter.set_pos(funcpos(letter.screenpos,i,len(letters)))
              for i,letter in enumerate(letters)]
    
    
main()