#!/usr/bin/env python

import RPi.GPIO as GPIO, time, datetime, math, rrdtool, feedparser, xml.sax, urllib2

#from Adafruit_MCP230xx import MCP230XX_GPIO
#from Adafruit_MCP230xx import Adafruit_MCP230XX 


DEBUG = 1

iTemperature=0
TIME_REFRESH = 1
TIME_ROUND = 2



GPIO.setmode(GPIO.BCM)

button = 0
#mcp= MCP23008()
#mcp = Adafruit_MCP230XX(busnum=1, address=0x20, num_gpios=8)

BIT_13 = 11
BIT_12 = 9
BIT_11 = 10
BIT_10 = 22
BIT_9 = 27
BIT_8 = 17
BIT_7 = 4
BIT_6 = 3
BIT_5 = 2
BIT_4 = 7
BIT_3 = 8
BIT_2 = 15
BIT_1 = 14


SPICLK = 18
SPIMOSI = 24
SPIMISO = 23
SPICS = 25

GPIO.setup(BIT_8, GPIO.OUT)
GPIO.setup(BIT_7, GPIO.OUT)
GPIO.setup(BIT_6, GPIO.OUT)
GPIO.setup(BIT_5, GPIO.OUT)
GPIO.setup(BIT_4, GPIO.OUT)
GPIO.setup(BIT_3, GPIO.OUT)
GPIO.setup(BIT_2, GPIO.OUT)
GPIO.setup(BIT_1, GPIO.OUT)
GPIO.setup(BIT_9, GPIO.OUT)
GPIO.setup(BIT_10, GPIO.OUT)
#mcp.config(BIT_9, mcp.OUTPUT)
GPIO.setup(BIT_10, GPIO.OUT)
GPIO.setup(BIT_11, GPIO.OUT)
GPIO.setup(BIT_12, GPIO.OUT)

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

toursxml='http://weather.yahooapis.com/forecastrss?w=573760&u=c'

class ABContentHandler(xml.sax.ContentHandler):
  def __init__(self):
    xml.sax.ContentHandler.__init__(self)
 
  def startElement(self, name, attrs):
    global iTemperature
   
    if name == "yweather:condition":
      iTemperature=int(attrs.getValue("temp"))
  




def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 1) or (adcnum < 0)):
        return -1
    if (adcnum == 0):
            commandout = 0x6
    else:
            commandout = 0x7
    GPIO.output(cspin, True)
 
    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low
 
    #commandout = 0x6  #start bit and 1, 0 to select single ended ch0
    commandout <<= 5    # we only need to send 3 bits here
    for i in range(3):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
 
    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1
 
    GPIO.output(cspin, True)
 
    adcout /= 2       # first bit is 'null' so drop it
    return adcout

def buttonSleep(ttime):
	
	#print(GPIO.input(BITIN_1))
	time.sleep(ttime)
	

def outOn(bit):
	if bit==1:
		GPIO.output(BIT_1,True)
	if bit==2:
		GPIO.output(BIT_2,True)
	if bit==3:
		GPIO.output(BIT_3,True)
	if bit==4:
		GPIO.output(BIT_4,True)	
	if bit==5:
		GPIO.output(BIT_5,True)
	if bit==6:
		GPIO.output(BIT_6,True)
	if bit==7:
		GPIO.output(BIT_7,True)
	if bit==8:
		GPIO.output(BIT_8,True)
	if bit==9:
		GPIO.output(BIT_9,1)
	if bit==10:
		GPIO.output(BIT_10,1)
	if bit==11:
		GPIO.output(BIT_11,1)
	if bit==12:
		GPIO.output(BIT_12,1)

def outOff(bit):
	if bit==1:
		GPIO.output(BIT_1,False)
	if bit==2:
		GPIO.output(BIT_2,False)
	if bit==3:
		GPIO.output(BIT_3,False)
	if bit==4:
		GPIO.output(BIT_4,False)	
	if bit==5:
		GPIO.output(BIT_5,False)
	if bit==6:
		GPIO.output(BIT_6,False)
	if bit==7:
		GPIO.output(BIT_7,False)
	if bit==8:
		GPIO.output(BIT_8,False)
	if bit==9:
		GPIO.output(BIT_9,0)
	if bit==10:
		GPIO.output(BIT_10,0)
	if bit==11:
		GPIO.output(BIT_11,0)
	if bit==12:
		GPIO.output(BIT_12,0)
		
def tempBling():
	ret = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
	millivolts = ret * ( 3300.0 / 1024.0)

    # 10 mv per degree 
	temp_C = (millivolts / 10.0) - 50.0
	temp_R=int(round(temp_C))
	
	#temp_C = ((millivolts - 100.0) / 10.0) - 40.0
	if temp_C>=0:
		for x in range(1, 13):
			outOn(x)
			buttonSleep(0.02)
		for x in range(1, 13):
			outOff(x)
			buttonSleep(0.02)
	else:
		for x in range(1, 13):
			outOn(13-x)
			buttonSleep(0.02)
		for x in range(1, 13):
			outOff(13-x)
			buttonSleep(0.02)
	if (temp_C>0 and temp_C<=10):
		for x in range (1, temp_R+1):
			outOn(x)
	if (temp_C>10 and temp_C<=20):
		outOn(12)
		for x in range (1, temp_R-9):
			outOn(x)
	if (temp_C>20 and temp_C<=30):
		outOn(12)
		outOn(11)
		for x in range (1, temp_R-19):
			outOn(x)
	if (temp_C>30 and temp_C<=40):
		outOn(12)
		outOn(11)
		outOn(10)
		for x in range (1, temp_R-29):
			outOn(x)
		
	buttonSleep(TIME_REFRESH)
		#tunnit pois
	for x in range (1, 13):
		outOff(x)
	buttonSleep(TIME_ROUND)
	return temp_C

try:
	toursurl= urllib2.urlopen(toursxml)
	toursurl_string= toursurl.read()
	xml.sax.parseString(toursurl_string, ABContentHandler())
except:
	iTemperature=0
t0= time.time()	
start=1
while True:
	now = datetime.datetime.now()
	hhour = now.hour
	minute = now.minute
	second = now.second	
	
	itmp=str(iTemperature)
	
	if hhour>12:
		hour=hhour-12
	else:
		hour=hhour;
	if hour==0:
		hour=12
	
	#12 tunnin naytto
	if hhour>=12:
		for x in range(1, 13):
			outOn(x)
			buttonSleep(0.02)
			outOff(x)
	
	if hhour<12:
		for x in range(1, 13):
			outOn(13-x)
			buttonSleep(0.02)
			outOff(13-x)
	
	
	
	#tunnit paalle	
	for x in range (1, hour+1):
		outOn(x)
	buttonSleep(TIME_REFRESH)
	
	#tunnit pois
	for x in range (1, hour+1):
		outOff(x)
	buttonSleep(TIME_REFRESH)
	
	for x in range (1, (minute+1)/5+1):
		outOn(x)
	buttonSleep(TIME_REFRESH)
	
	for x in range (1, (minute+1)/5+1):
		outOff(x)
	buttonSleep(TIME_REFRESH)
	temps=str(tempBling())
	#print(temps +' x '+ itmp)
	buttonSleep(TIME_REFRESH)
	rrdtool.update('tempbase2.rrd','N:' + temps + ':' +itmp)
	
	t=time.time()
	#print(t-t0)
	if (t-t0)>300 or start==1:
		try:
			toursurl= urllib2.urlopen(toursxml)
			toursurl_string= toursurl.read()
			xml.sax.parseString(toursurl_string, ABContentHandler())
		except:
			iTemperature=0
		t0=t
		start=0
		#print("----------")
		#print(t)
		#print(t0)
	
