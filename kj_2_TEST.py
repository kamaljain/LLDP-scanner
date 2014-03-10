#!/usr/bin/python
import os
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

import signal
import sys

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        lcd.clear()
        lcd.backlight(lcd.OFF)
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Clear display and show startup message
lcd.clear()
lcd.message("SEL=LITE LFT=IP\nUP/DOWN=SCROLL DATA")

# Poll buttons, display message & set backlight accordingly
btn = ((lcd.LEFT  , '/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/kj_LEFT.txt'),
       (lcd.UP    , '/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/kj_UP.txt'),
       (lcd.DOWN  , '/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/kj_DOWN.txt'),
       (lcd.RIGHT , '/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/kj_RIGHT.txt'),
       (lcd.SELECT, '/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/kj_SELECT.txt'))
prevBtn = -1
prevBacklight = lcd.ON
while True:
    for b in btn:
        if lcd.buttonPressed(b[0]):
            if b is not prevBtn or b[0] == lcd.SELECT:
                if b[0] == lcd.LEFT:
                    os.system('ifconfig eth0 | awk \'/inet addr/ {print substr($2,6),"\\n"substr($4,6)}\' > /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/kj_LEFT.txt')
                if b[0] == lcd.SELECT:
                    if prevBacklight == lcd.ON:
                        lcd.backlight(lcd.OFF)
                        prevBacklight = lcd.OFF
                    else:
                        lcd.backlight(lcd.ON)
                        prevBacklight = lcd.ON
		if b[0] == lcd.DOWN:
		    os.system('/bin/bash /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/gather_llinfo.sh')
#		    subprocess.call("/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/gather_llinfo.sh", shell=True)
                if b[0] is not lcd.SELECT:
                    lcd.clear()
                    f = open(b[1], 'r')
                    line1 = f.readline()
                    line2 = f.readline()
                    lcdmsg = line1+line2
                    print 'line1 = ', line1
                    print 'line2 = ', line2
                    print 'lcdmsg = ', lcdmsg
                    lcd.message(lcdmsg)
                prevBtn = b
                sleep(0.2)
            break
