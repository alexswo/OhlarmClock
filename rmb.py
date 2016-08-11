#!/usr/bin/python
#
# HD44780 LCD/OLED Test Script for
# Raspberry Pi
#
# Author : Robert Coward (based on driver by Matt Hawkins/)
# Site   : http://www.raspberrypi-spy.co.uk
# 
# Date   : 27/02/2014
#

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping
LCD_RS = 25
LCD_E  = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 27
LCD_D7 = 22

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants for low level write operations
# NOTE: Enable cycle time must be at least 1 microsecond 
# NOTE2: Actually, these can be zero and the LCD will typically still work OK
EDEL_TAS =  0.00001      # Address setup time (TAS)
EDEL_PWEH = 0.00001      # Pulse width of enable (PWEH)
EDEL_TAH =  0.00001      # Address hold time (TAH)

# Timing constraints for initialisation steps - IMPORTANT!
# Note that post clear display must be at least 6.2ms for OLEDs, as opposed
# to only 1.4ms for HD44780 LCDs. This has caused confusion in the past.
DEL_INITMID = 0.01       # middle of initial write (min 4.1ms)
DEL_INITNEXT = 0.0002     # post ssecond initial write (min 100ns)
DEL_POSTCLEAR = 0.01       # post clear display step (busy, min 6.2ms)

# ==============================================================================
# LCD Initialisation to setup the two line display using the 4 bit interface

def lcd_init():
  # Configure the GPIO to drive the LCD display correctly
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

  # setup all output pins for driving LCD display
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  
  # Initialise display into 4 bit mode, using recommended delays
  lcd_byte(0x33,LCD_CMD, DEL_INITNEXT, DEL_INITMID)
  lcd_byte(0x32,LCD_CMD, DEL_INITNEXT)
  
  # Now perform remainder of display init in 4 bit mode - IMPORTANT!
  # These steps MUST be exactly as follows, as OLEDs in particular are rather fussy
  lcd_byte(0x28,LCD_CMD, DEL_INITNEXT)    # two lines and correct font
  lcd_byte(0x08,LCD_CMD, DEL_INITNEXT)    # display OFF, cursor/blink off
  lcd_byte(0x01,LCD_CMD, DEL_POSTCLEAR)    # clear display, waiting for longer delay
  lcd_byte(0x06,LCD_CMD, DEL_INITNEXT)    # entry mode set

  # extra steps required for OLED initialisation (no effect on LCD)
  lcd_byte(0x17,LCD_CMD, DEL_INITNEXT)    # character mode, power on

  # now turn on the display, ready for use - IMPORTANT!
  lcd_byte(0x0C,LCD_CMD, DEL_INITNEXT)    # display on, cursor/blink off

# ==============================================================================
# Outputs string o characters to the LCD display line, padding as required

def lcd_string(message):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")  

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

# ==============================================================================
# Low level routine to output a byte of data to the LCD display
# over the 4 bit interface. Two nybbles are sent, one after the other.
# The post_delay specifies optional delay to cover busy periods
# The mid_delay specifies optional delay between the 4  bit nibbles (special case)

def lcd_byte(byteVal, mode, post_delay = 0, mid_delay = 0):

  # convert incoming value into 8 bit array, padding as required
  bits = bin(byteVal)[2:].zfill(8)
  
  # generate an array of pin numbers to write out
  lcdPins = [LCD_D7, LCD_D6, LCD_D5, LCD_D4]

  # set mode = True  for character, False for command
  GPIO.output(LCD_RS, mode) # RS

  # Output the four High bits
  for i in range(4):
    GPIO.output(lcdPins[i], int(bits[i]))

  # Toggle 'Enable' pin, wrapping with minimum delays
  time.sleep(EDEL_TAS)    
  GPIO.output(LCD_E, True)  
  time.sleep(EDEL_PWEH)
  GPIO.output(LCD_E, False)  
  time.sleep(EDEL_TAH)      

  # Wait for extra mid delay if specified (special case)
  if mid_delay > 0:
    time.sleep(mid_delay)

  # Output the four Low bits
  for i in range(4,8):
    GPIO.output(lcdPins[i-4], int(bits[i]))

  # Toggle 'Enable' pin, wrapping with minimum delays
  time.sleep(EDEL_TAS)    
  GPIO.output(LCD_E, True)  
  time.sleep(EDEL_PWEH)
  GPIO.output(LCD_E, False)  
  time.sleep(EDEL_TAH)   

  # Wait for extra post delay if specified (covers busy period)
  if post_delay > 0:
    time.sleep(post_delay)

# ==============================================================================
# main routine which initialises the display and outputs text messages to it

def main():
  # Initialise GPIO port and display 
  lcd_init()
  for x in range (0,50):
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Rasbperry Pi")
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("Model B" + str(x))
  # Send some text
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Rasbperry Pi")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("Model B")

  time.sleep(3) # 3 second delay

  # Send some more text
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Raspberrypi-spy")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string(".co.uk")

  time.sleep(3) # 3 second delay

  # Send some more text
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Modified by")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("Robert Coward")

  time.sleep(3) # 3 second delay

  # Send some more text
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("1234567890!$%^&*()")

# ==============================================================================
# Ensure that the GPIO is cleaned up whichever way the program exits
# This avoids all those annoying "channel already in use" errors

if __name__ == '__main__':
  try:
    main()
  finally: GPIO.cleanup()

# ==============================================================================
# ==============================================================================
