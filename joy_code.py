import time
import os
import RPi.GPIO as GPIO
import sys
import signal
import joy_objects
from joy_oop import Joystick, Vector2, SerialIn, Snake, FoodList

def signal_handler(signal, frame):
	sys.exit(0)

GPIO.setmode(GPIO.BCM)
DEBUG = 1
joystick1 = Joystick(18, 23, 24, 25, 0, 1, 22)
Python = Snake(1)
print "origin", joystick1.PrintOrigin()
time.sleep(2)
while True:
	joystick1.run()