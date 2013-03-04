import time
import os
import RPi.GPIO as GPIO
import sys
import signal

GPIO.setmode(GPIO.BCM)
DEBUG = 1
def signal_handler(signal, frame):
	sys.exit(0)

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if(adcnum > 1) or (adcnum < 0)):
		return -1
	GPIO.output(cspin, True)
	GPIO.output(clockpin, False)
	GPIO.output(cspin, False)

	commandout = adcnum
	commandout |= 0x18
	commandout <<=3
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
		if(GPIO.input(misopin)):
			adcout |= 0x1
	adcout >>=1
	return adcout

SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

timer = 0

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

horizontal_adc = 0
vert_adc = 1
Xpos = 0
Ypos = 0

originX = readadc(horizontal_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
originY = readadc(vert_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

while True:
	hori_changed = False
	vert_changed = False

	hori_pot = readadc(horizontal_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	vert_pot = readadc(vert_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

	if(hori_adjust > 24 or hori_adjust < -120):
		Xpos = Xpos + hori_adjust
		hori_changed = True
	if(vert_adjust > 24 or vert_adjust < -20):
		Ypos = Ypos + vert_adjust
		vert_changed = True
	if hori_changed:
		print 'new xpos:', Xpos
		print 'movement:', hori_adjust
	if vert_changed:
		print 'new Y position:', Ypos
		print 'movement:', vert_adjust
			
	# escape clause: I got bored of having the program run 4ever, so this line (and the method defined earlier) means that if you press ctrl + c, the program
	#will stop...at its earliest convenience.
	signal.signal(signal.SIGINT, signal_handler)