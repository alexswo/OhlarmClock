#!usr/bin/env python

#18 -- LED -->6
#22 -- Button -->5

import RPi.GPIO as GPIO
import RPi.GPIO as GPIO
import time

class button:
	#Initialize LED process
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(6, GPIO.OUT)
		GPIO.output(6,GPIO.HIGH)
		GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	#Confirm if a button was pressed. 
	def buttonPressed(self):
		return GPIO.input(5)
