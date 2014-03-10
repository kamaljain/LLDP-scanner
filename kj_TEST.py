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
        print '\n\nCtrl+C pressed - exiting'
        lcd.clear()
        lcd.backlight(lcd.OFF)
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Clear display and show startup message
lcd.backlight(lcd.OFF)
lcd.clear()
lcd.message("SEL=LITE LFT=IP\nDWN=LLDP UP=MENU")

# Poll buttons, display message & set backlight accordingly
btn = ((lcd.LEFT  , '/home/lldp/kj_LEFT.txt'),
       (lcd.UP    , '/home/lldp/kj_UP.txt'),
       (lcd.DOWN  , '/home/lldp/kj_DOWN.txt'),
       (lcd.RIGHT , '/home/lldp/kj_RIGHT.txt'),
       (lcd.SELECT, '/home/lldp/kj_SELECT.txt'))
prevBtn = lcd.UP
prevBacklight = lcd.OFF
while True:
    for b in btn:
        if lcd.buttonPressed(b[0]):

            if b[0] == lcd.SELECT:
                if prevBacklight == lcd.ON:
                    lcd.backlight(lcd.OFF)
                    prevBacklight = lcd.OFF
                else:
                    lcd.backlight(lcd.ON)
                    prevBacklight = lcd.ON

            if b[0] == lcd.LEFT:
                os.system('/bin/bash /home/lldp/gather_ipinfo.sh')

            if b[0] == lcd.DOWN:
                os.system('/bin/bash /home/lldp/gather_llinfo.sh')

            if b[0] is not lcd.SELECT and b[0] is not lcd.RIGHT:
                lcd.clear()
                f = open(b[1], 'r')
                line1 = f.readline()
                line2 = f.readline()
                lcdmsg = line1+line2
# Next few print statements are for debug output
#                print 'line1 = ', line1
#                print 'line2 = ', line2
#                print 'lcdmsg = \n', lcdmsg
                lcd.message(lcdmsg)
                f.close()

            if b[0] == lcd.RIGHT:
                    lcd.clear()
                    os.system('/bin/bash /home/lldp/gather_ipinfo.sh')
#                    f = open(b[1], 'r')
                    f = open('/home/lldp/kj_LEFT.txt', 'r')
                    line1 = f.readline()
                    line2 = f.readline()
                    lcdmsg = line1+line2
                    lcd.message(lcdmsg)
                    f.close()

                    sleep(2)

                    lcd.clear()
                    os.system('/bin/bash /home/lldp/gather_llinfo.sh')
#                    f = open(b[1], 'r')
                    f = open('/home/lldp/kj_DOWN.txt', 'r')
                    line1 = f.readline()
                    line2 = f.readline()
                    lcdmsg = line1+line2
                    lcd.message(lcdmsg)
                    f.close()

                    sleep(2)


            prevBtn = b
            sleep(0.3)

#        else:
#            while [ prevBtn != lcd.RIGHT ]:
#                if b[0] == lcd.LEFT:
#                    os.system('/bin/bash /home/lldp/gather_ipinfo.sh')
#    
#                if b[0] == lcd.DOWN:
#                    os.system('/bin/bash /home/lldp/gather_llinfo.sh')
#    
#                if b[0] is not lcd.SELECT:
#                    lcd.clear()
#                    f = open(b[1], 'r')
#                    line1 = f.readline()
#                    line2 = f.readline()
#                    lcdmsg = line1+line2
#                    lcd.message(lcdmsg)
#                    f.close()
#
##            break
#    
#            sleep(1)
#
#        break
