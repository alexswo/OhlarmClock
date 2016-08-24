#!/usr/bin/env python

#Data Sheet for Menu -- Menu Location is Navigated Numerically
#Use the Rotary Encoder to Increment or Decrement between menu selections.   
#0 - Main Menu (i.e. date and temperatue; 12/27/1995 \n High:78 Low:60)
#1 - Volume Menu (i.e. Volume level; Volume: \n 70)
#More to Come Later. . . 

import time
from datetime import datetime
import pytz
import oled_class 
import RPi.GPIO as GPIO

#For Weather
import urllib2
import json

cursorLocation = 0
modifyingVolume = 0
LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0
LCD_CMD = False
stringOfCurrentDate = 0
high = 0
low = 0
initMenu = False

zero = 00
fifteen = 15
thirty = 30
fourtyfive = 45

condition = 0

choosingDate = 0
choosingTimeH = 0
cursorForDate = 0
choosingTimeM = 0
alarmHour = 0
alarmMinute = 0
strAlarmHour = " "  
strAlarmMin = " " 
alarmString = " " 
class menu_class:

	def __init__(self):
		self.oled = oled_class.oled_class()
		self.location = pytz.timezone("America/Los_Angeles")
		self.dateFmt = '%m/%d/%Y'
		self.timeFmtMinutes = '%M'
		self.mainMenu()
	def navigateMenu(self, cursor, callback):
		#Cursor holds value of 0,1,2
		#2 -- Left
		#1 -- Right
		#3 -- Select (i.e. when button is pushed)
		global modifyingVolume
		global choosingDate
		global choosingTimeH 
		global choosingTimeM
		self.callback = callback
		
		if(modifyingVolume == 1 and cursor == 2):
			self.volumeMenu(0)
		elif(modifyingVolume == 1 and cursor == 1):
			self.volumeMenu(1)
		elif(choosingDate == 1 and cursor == 2):
			self.alarmMenu(0)
		elif(choosingDate == 1 and cursor == 1):
			self.alarmMenu(1)
		elif(choosingTimeH == 1 and cursor == 2):
			self.alarmMenu(0)
		elif(choosingTimeH == 1 and cursor == 1):
			self.alarmMenu(1)
		elif(choosingTimeM == 1 and cursor == 2):
			self.alarmMenu(0)
		elif(choosingTimeM == 1 and cursor == 1):
			self.alarmMenu(1)
		elif(cursor == 2):
			if(cursorLocation == 0):
				self.alarmMenu(0)
			elif(cursorLocation == 1):
				self.mainMenu()
			elif(cursorLocation == 2):
				self.volumeMenu(0)
		elif(cursor == 1):
			if(cursorLocation == 0):
				self.volumeMenu(0)
			elif(cursorLocation == 1):
				self.alarmMenu(0)
			elif(cursorLocation == 2):
				self.mainMenu()
		elif(cursor == 3):
			if(cursorLocation == 1 and modifyingVolume == 0):
				modifyingVolume = 1
			elif(cursorLocation == 1 and modifyingVolume == 1):
				modifyingVolume = 0
			elif(cursorLocation == 2 and choosingDate == 0 and choosingTimeH == 0 and choosingTimeM == 0):
				choosingDate = 1
				self.alarmMenu(2)
			elif(cursorLocation == 2 and choosingDate == 1 and choosingTimeH == 0):
				choosingDate = 0
				choosingTimeH = 1
				self.alarmMenu(2)
				print "Hello 1!"
			elif(cursorLocation == 2 and choosingTimeH == 1):
				choosingTimeH = 0 
				choosingTimeM = 1
				print "Hello 2!"
				self.alarmMenu(2)
			elif(cursorLocation == 2 and choosingTimeM == 1):
				choosingTimeM = 0 
				self.alarmMenu(2)
	def cancelBtn(self):
		global choosigDate
		global choosingTimeH
		global choosingTimeM
		if(cursorLocation == 2):
			choosingDate = 0
			choosingTimeH = 0 
			choosingTimeM = 0
			self.alarmMenu(2)
	def alarmMenu(self, leftOrRight):
		#0 -- Left
		#1 -- Right
		global cursorLocation
                global LCD_LINE_1
                global LCD_LINE_2
                global LCD_CMD	
		global choosingDate
		global cursorForDate
		global choosingTimeH
		global choosingTimeM
		global alarmHour
		global alarmMinute
		global strAlarmHour
		global strAlarmMin
		global alarmString
		cursorLocation = 2
		if(choosingDate == 1):
			if(leftOrRight == 0):
				if(cursorForDate == 0):
					cursorForDate = 6
				else:
					cursorForDate = cursorForDate - 1
			elif(leftOrRight == 1):
				if(cursorForDate == 6):
					cursorForDate = 0
				else:
					cursorForDate = cursorForDate + 1
			space = " "
                	if(cursorForDate == 0):
                        	space = " ^^"
                	elif(cursorForDate == 1):
                        	space = "    ^"
                	elif(cursorForDate == 2):
                        	space = "      ^"
                	elif(cursorForDate == 3):
                        	space = "        ^"
                	elif(cursorForDate == 4):
                        	space = "          ^"
                	elif(cursorForDate == 5):
                        	space = "            ^"
                	elif(cursorForDate == 6):
                        	space = "              ^^"

                	self.oled.lcd_byte(LCD_LINE_1, LCD_CMD)
                	self.oled.lcd_string(" SN M T W R F ST")
                	self.oled.lcd_byte(LCD_LINE_2, LCD_CMD)
               		self.oled.lcd_string(space)
                	time.sleep(.2)
	
		elif(choosingTimeH == 1):
			if(leftOrRight == 0):
				if(alarmHour == 0):
					alarmHour = 24
				else:
					alarmHour = alarmHour - 1
			elif(leftOrRight == 1):
				if(alarmHour == 24):
					alarmHour = 0
				else:
					alarmHour = alarmHour + 1
			if(alarmHour <= 9):
				strAlarmHour = "0" + str(alarmHour)
			else:
				strAlarmHour = str(alarmHour)
			self.oled.lcd_byte(LCD_LINE_1, LCD_CMD)
                	self.oled.lcd_string(strAlarmHour + ":00 ")
               		self.oled.lcd_byte(LCD_LINE_2, LCD_CMD)
               		self.oled.lcd_string("^^")
			time.sleep(.2)
		elif(choosingTimeM == 1):
			if(leftOrRight == 0):
				if(alarmMinute == 0):
					alarmMinute = 60
				else:
					alarmMinute = alarmMinute - 1
			elif(leftOrRight == 1):
				if(alarmMinute == 60):
					alarmMinute = 0
				else:
					alarmMinute = alarmMinute + 1
			if(alarmMinute <= 9):
				strAlarmMin = "0" + str(alarmMinute)
			else:
				strAlarmMin = str(alarmMinute)
			alarmString = strAlarmHour + ":" + strAlarmMin
		        self.oled.lcd_byte(LCD_LINE_1, LCD_CMD)
                        self.oled.lcd_string(alarmString)
                        self.oled.lcd_byte(LCD_LINE_2, LCD_CMD)
                        self.oled.lcd_string("   ^^")
                        time.sleep(.2)
		else: 
			with open('data.cfg','r') as file:
				data = file.readlines()
			data[cursorForDate] = alarmString + '\n'
			with open('data.cfg','w') as file:
				file.writelines(data)
			alarmMinute = 0
			alarmHour = 0
			self.oled.lcd_byte(LCD_LINE_1, LCD_CMD)
                	self.oled.lcd_string("    Set Alarm")
                	self.oled.lcd_byte(LCD_LINE_2, LCD_CMD)
                	self.oled.lcd_string("")
			time.sleep(.2)					
	def mainMenu(self):
			#Make calls to the 16x2 display and update it.
		global cursorLocation
		global LCD_LINE_1
		global LCD_LINE_2
		global LCD_CMD
		global stringOfCurrentDate
		global low
		global high
		cursorLocation = 0
		currentDate = datetime.now(self.location)
		stringOfCurrentDate = currentDate.strftime(self.dateFmt)

#		GPIO.cleanup()
		self.oled.lcd_byte(LCD_LINE_1, LCD_CMD)
		self.oled.lcd_string("   "+stringOfCurrentDate)
		self.oled.lcd_byte(LCD_LINE_2, LCD_CMD)
		self.oled.lcd_string(" High:" + str(high) + " " + "Low:" + str(low))
		print "Spinning..."
		time.sleep(.2)
		#print stringOfCurrentDate
	def volumeMenu(self, leftOrRight):
		global cursorLocation
		global modifyingVolume
                global LCD_LINE_1
                global LCD_LINE_2
                global LCD_CMD
		cursorLocation = 1
		if(modifyingVolume):
			if(leftOrRight == 0):
				self.callback.adjustVolume(0)
			elif(leftOrRight == 1):
				self.callback.adjustVolume(1)
		#this calls back to media.adjustVolume -- which is in the file musicPlayer.py
#		GPIO.cleanup()
		self.oled.lcd_byte(LCD_LINE_1, LCD_CMD)
                self.oled.lcd_string("Volume Lvl:")
                self.oled.lcd_byte(LCD_LINE_2, LCD_CMD) 
                self.oled.lcd_string(str(self.callback.getVolume()))
		print "Spinning . . . ."
		time.sleep(.2)
	def cursorOnMainMenu(self):
		return cursorLocation
	def updateMenu(self):
		global stringOfCurrentDate
		global high
		global low
		global initMenu
		global zero
		global fifteen
		global thirty
		global fourtyfive
		global condition

		currentDate = datetime.now(self.location)
		stringOfUpdatingTime = currentDate.strftime(self.timeFmtMinutes)
		if(stringOfUpdatingTime == zero or stringOfUpdatingTime == fifteen or stringOfUpdatingTime == thirty or stringOfUpdatingTime == fourtyfive or initMenu == False):
			key = "45170d9e98bbbe56"
			zip = '90020'
			url = 'http://api.wunderground.com/api/' + key + '/geolookup/forecast10day/q/' + zip + '.json'
			f = urllib2.urlopen(url)
			json_string = f.read()
			parsed_json = json.loads(json_string)
			high =  parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
			print 'High: ' + high
			low  =  parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
			print 'Low: ' + low
			condition = parsed_json['forecast']['simpleforecast']['forecastday'][0]['conditions']
			print 'The condition is ' + condition
			f.close()
			self.mainMenu()
			initMenu = True
