import time
import os
import RPi.GPIO as GPIO
import sys
import signal

GPIO.setmode(GPIO.BCM)

def signal_handler(signal, frame):
	sys.exit(0)


def readadc(adcnum, clockpin, mosipin, misopin, cspin):

	#CODE WRITTEN BY ADAFRUIT: I don't know enough python to have done this tutorial alone.
	if(adcnum > 1) or (adcnum < 0):
		return -1
	
	GPIO.output(cspin, True)
	GPIO.output(clockinp, False)
	GPIO.output(cspin, False)
	
	commandout = adcnum
	commandout |= 0x18
	
	for i in range(5):
		if(commandout & 0x80):
			GPIO.output(mosipin, True)
		else:
			GPIO.output(mosipin, False)
		commandout <<=1
		
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
	adcout = 0
	for i in range(12):
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
		adcout <<= 1
		if(GPIO.input(misopin)):
			adcout |= 0x1
	adcout >>=1
	return adcout

#our pins - if you've changed where anything got plugged in to the cobbler/pi, change these numbers
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#again, if you've changed which channel you're using for which, change these
horizontal_adc = 0
vert_adc = 1

#starting x and y values
Xpos = 0
Ypos = 0

#where the actual joystick rests when it's upright
originX = readadc(horizontal_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
originY = readadc(vert_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

while True:
	hori_changed = False
	vert_changed = False
	
	#take in the input
	hori_pot = readadc(horizontal_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	vert_pot = readadc(vert_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	
	#calculate the difference between the current position and the origin
	hori_adjust = abs(hori_pot - originX)
	vert_adjust = abs(vert_pot - originY)
	
	#calculate the new position
	Xpos = Xpos + hori_adjust
	Ypos = Ypos + vert_adjust
	
	#for me, I found that at rest it was continually moving by 16. This may be because the joystick is not sitting flat. The number may be different for you
	#takes a bit of testing to figure it out
	if(hori_adjust > 16):
		hori_changed = True
	if(vert_adjust > 16):
		vert_changed = True
		
		#if there's been a changed, print the new position and how much it's moved by
		if hori_changed:
			print 'new X position:', Xpos
			print 'movement:', hori_adjust
		if vert_changed:
			print 'new Y position:', Ypos
			print 'movement:', vert_adjust
			
	# escape clause: I got bored of having the program run 4ever, so this line (and the method defined earlier) means that if you press ctrl + c, the program
	#will stop...at its earliest convenience.
	signal.signal(signal.SIGINT, signal_handler)