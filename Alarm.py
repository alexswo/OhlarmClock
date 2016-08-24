#!/usr/bin/env python

from datetime import datetime
import pytz # $ pip install pytz
import time as t
import linecache
import musicPlayer
import button
import subprocess 
import sys
from rotary_class import RotaryEncoder
import menu_class
import sevenSegmentFunc

#subprocess.call("/home/pi/OhlarmClock/rmb.py",shell=True)
#subprocess.call("/home/pi/OhlarmClock/rmb2.py",shell=True)

media = musicPlayer.musicPlayer()
menu = menu_class.menu_class()
button = button.button()
sevenSegment = sevenSegmentFunc.sevenSegmentFunc()

#Defining GPIO Pins for each switch related to the Rotary Encoder
BUTTON_SWITCH = 19
LEFT_SWITCH = 16
RIGHT_SWITCH = 12
volumeknob = RotaryEncoder(LEFT_SWITCH,RIGHT_SWITCH,BUTTON_SWITCH,menu.navigateMenu,media)

#This subprocess call will make the 3.5mm  audio jack the primary target
#for outputting audio from.
#subprocess.call("/home/pi/Projects/audioJack.sh", shell=True)

#These two commands are for getting the data that are listed on the data.cfg 
alarmTime1 = linecache.getline("data.cfg", 2).rstrip('\n')
alarmTime2 = linecache.getline("data.cfg", 3).rstrip('\n')

while(1): 
    #buttonPressed() returns a 'False' when a button IS pressed. 
    if button.buttonPressed() == False:
	menu.cancelBtn()
	media.exitAlarm()
#    print "The time is: " +  sevenSegment.getTime()
#    print "The alarm is:" +  alarmTime1 
#    if(alarmTime1 == sevenSegment.getTime()): #Change this afterwards
#        media.soundAlarm()
#    if(True):
#        media.soundAlarm()
#	print "HEllo!"
    sevenSegment.setSSDisplay()
    menu.updateMenu()
    t.sleep(0.000000000005)

