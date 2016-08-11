#!/usr/bin/env python
from Adafruit_LED_Backpack import SevenSegment
from datetime import datetime
import pytz
import time as t
class sevenSegmentFunc:
	def __init__(self):
		#Controlling the Seven Segment Display
		self.display = SevenSegment.SevenSegment() #Create display instance on default I2C address (0x70) and bus$
		self.display.begin() # Initialize the display. Must be called once before using the display.
		self.location = pytz.timezone("America/Los_Angeles")
		self.timeFmt24 = '%H:%M'
	def setSSDisplay(self):
		time = datetime.now(self.location)
		timeString = time.strftime(self.timeFmt24)		
		timeFmt24Obj = t.strptime(timeString, "%H:%M")
		timeFmt12 = t.strftime("%I.%M", timeFmt24Obj)
		self.display.clear()
		self.display.print_float(float(timeFmt12))
		self.display.set_colon(True)
		self.display.write_display()
	def getTime(self):
		time = datetime.now(self.location)
		timeString = time.strftime(self.timeFmt24)
		return timeString
