#!/usr/bin/env python

'''
 ^H> HucDuino 22-12-2018

  web-lcd 

  https://github.com/dbrgn/RPLCD
'''

from flask import Flask
from flask import render_template, request
from RPLCD.i2c import CharLCD
from time import *
import subprocess

lcd = CharLCD('PCF8574', 0x27)

"""
lcd = CharLCD(i2c_expander='PCF8574', address=0x29, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)
"""

HOST = '0.0.0.0'              # server adres
PORT = 5000                   # server poort
HUC = 'HucDuino'              # 
LOGO = '^H>'                  # logo text
TITLE = 'Web Control to LCD'  #
TITLE2 = '404'                # title 404.html
DEMO = 'Hello World'          #  

pi_model1 = subprocess.check_output("cat /proc/device-tree/model | awk '{print $1 , $2'}", shell=True)
pi_model2 = subprocess.check_output("cat /proc/device-tree/model | awk '{print $3 , $4 , $5 , $6'}", shell=True)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title=TITLE, logo=LOGO, huc=HUC)


@app.route("/change", methods=['POST'])
def change():
    if request.method == 'POST':
        # Get the value from the submitted form
        lcdText = request.form['lcd']
        lcdText2 = request.form['lcd2']
        print "---Message line 1 is :", lcdText
        print "---Message line 2 is :", lcdText2
        
        # Send the message to the LCD
        lcd.clear()
        lcd.cursor_mode = 'hide' 
        lcd.cursor_pos = (0, 0)
        lcd.write_string(lcdText)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(lcdText2)
    else:
        lcdText = None
        lcdText2 = None
    return render_template('index.html', title=TITLE, logo=LOGO, huc=HUC, value=lcdText , value2=lcdText2)

@app.route("/switch_lcd", methods=['POST'])
def lcd_handler():
    if request.form['btnlcd'] == "On":
        print("On")       # do On action
        lcd.backlight_enabled = True
    elif request.form['btnlcd'] == "Off":
        print("Off")      # do Off action
        lcd.backlight_enabled = False        
    elif request.form['btnlcd'] == "Clear":
        print("Clear")      # do Clear action
        lcd.cursor_mode = 'hide'
        lcd.clear()
        
    elif request.form['btnlcd'] == "Date":
        print("=Date")             # do Time action
        lcd.clear()
        lcd.cursor_mode = 'hide'        
        lcd.cursor_pos = (0, 0)
        lcd.write_string(strftime('%H:%M:%S'))
        lcd.cursor_pos = (1, 5)
        lcd.write_string(strftime('%d %b %Y'))       
        
    elif request.form['btnlcd'] == "Hello World":
        print("=Hello World")      # do Hello World action
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(DEMO)
        lcd.cursor_pos = (1, 2)
        lcd.write_string(LOGO)
        lcd.cursor_pos = (1, 6)
        lcd.write_string(HUC)
        lcd.cursor_pos = (1, 15)
        lcd.cursor_mode = 'blink'        
    elif request.form['btnlcd'] == "RPi Model":
        print("RPi Model")         # do RPi Model action
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(pi_model1)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(pi_model2)
        lcd.cursor_pos = (1, 15)
        lcd.cursor_mode = 'blink'               
    return render_template('index.html', title=TITLE, logo=LOGO, huc=HUC)

@app.errorhandler(404)
def page_not_found(e):
      return render_template('404.html', title2=TITLE2, logo=LOGO, huc=HUC), 404
     
if __name__ == "__main__":
    app.debug = True
    app.run(host=HOST, port=PORT, debug=True)

