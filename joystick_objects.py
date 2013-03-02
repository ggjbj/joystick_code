import time
import os
import RPi.GPIO as GPIO
import sys
import signal
import array
import random

class Vector2(object):
	def __init__(self, xPos, yPos):
		Vector2.x = xPos
		Vector2.y = yPos
	
	def GetX(self):
		return Vector2.x
	def GetY(self):
		return Vector2.y
	
	def SetX(self, _x):
		Vector2.x = _x
	def SetY(self, _y):
		Vector2.y = _y
	
	def multiply(self, newVector):
		newX = Vector2.x * newVector.GetX()
		newY = Vector2.y - newVector.GetY()
		vector = Vector2(newX, newY)
		return vector
	
	def difference(self, newVector):
		newX = Vector2.x - newVector.GetX()
		newY = Vector2.y - newVector.GetY()
		vector = Vector2(newX, newY)
		return vector
	
	def add(self, newVector):
		newX = Vector2.x + newVector.GetX()
		newY = Vector2.y + newVector.GetY()
		vector = Vector2(newX, newY)
		return vector
	
	def negative(self):
		return Vector2(-Vector2.GetX(), -Vector2.GetY())

class SerialIn(object):
	def __init__(self, clockpin, mosipin, misopin, cspin):
		SerialIn.clockpin = clockpin
		SerialIn.mosipin = mosipin
		SerialIn.misopin = misopin
		SerialIn.cspin = cspin
		GPIO.setup(mosipin, GPIO.OUT)
		GPIO.setup(mispin, GPIO.IN)
		GPIO.setup(clockpin, GPIO.OUT)
		GPIO.setup(cspin, GPIO.OUT)
	
	def read(self, adcnum):
		if((adcnum > 1) or (adcnum < 0)):
			return -1
		GPIO.output(SerialIn.cspin, True)
		GPIO.output(SerialIn.clockpin, False)
		GPIO.output(SerialIn.cspin, False)
	
		commandout = adcnum
		commandout |= 0x18
		commandout <<=3
		for i in range(5):
			if(commandout & 0x80):
				GPIO.output(SerialIn.mosipin, True)
				else:
					GPIO.output(SerialIn.mosipin, False)
				commandout <<=1
				GPIO.output(SerialIn.clockpin, True)
				GPIO.output(SerialIn.clockpin, False)
			adcout = 0
			for i in range(12):
				GPIO.output(SerialIn.clockpin, True)
				GPIO.output(SerialIn.clockpin, False
				adcout <<= 1
				if(GPIO.input(SerialIn.misopin)):
					adcout |= 0x1
			adcout >>=1
		return adcout
		
class Joystick(SerialIn):
	def __init__(self, clockpin, mosipin, misopin, cspin, hori_adc, vert_adc, selPin):
		SerialIn.__init__(self, clockpin, mosipin, misopin, cspin)
		Joystick.hori = hori_adc
		Joystick.vert = vert_adc
		Joystick.select = selPin
		Joystick.position = Vector2(0, 0)
		GPIO.setup(Joystick.select, GPIO.IN)
		Joystick.origin = Vector2(SerialIn, read(self, hori_adc), SerialIn.read(self, vert_adc))
	
	def readAxis(self):
		x = SerialIn.read(self, Joystick.hori)
		print "x", x
		time.sleep(1)
		y = SerialIn.read(self, Joystick.vert)
		print "y", y
		return Vector2(x, y)
		
	def PrintOrigin(self);
		print Joystick.origin.GetX(), " ", Joystick.origin.GetY()
	
	def run(self):
		hori_changed = False
		vert_changed = False
		
		reading = Joystick.readAxis(self)
		
		adjust = reading.difference(Joystick.origin)
		
		if(adjust.GetX() > 24 or adjust.GetX() < -120):
			Joystick.position.SetX(Joystick.position.GetX() + adjust.GetX())
			hori_changed = True
		if(adjust.GetY() > 24 or adjust.GetY() < -20):
			Joystick.position.GetY(Joystick.position.GetY() + adjust.GetY())
			vert_changed = True
		
		if hori_changed:
			print 'new x pos: ', Joystick.position.GetX()
			print 'movement: ', hori_adjust
		if vert_changed:
			print 'new y pos:', Joystick.position.GetY()
			print 'movement: ', vert_adjust
	
class Snake(object):
	def __init(self):
		Snake.body = list()
		Snake.body.append(Vector2(0, 0))
		Snake.direction = Vector2(0, 0)
		Snake.speed = Vector2(0, 0)
	
	def run(self, list):
		for item in Snake.body:
			item = Snake.direction.multiply(Snake.speed).add(item)
		Snake.bite(self, list)
	
	def bite(self, FoodList):
		newPos = Snake.body[-1]
		newPos = newPos.add(Snake.direction.negative(self))
		for item in FoodList:
			if(Snake.body[0].intersects(self, item)):
				Snake.body.append(newPos)
				FoodList.remove(item)
	
class FoodList(list):
	def __init__(self, posList):
		list.__init__(self)
		FoodList.extend(self, posList)
	
	def add(self, SnakeBody):
		#set an initial position
		x = random.randrange(0, 9)
		y = random.randrange(0, 9)
		positioned = False
		positionedProper = False
		for item in SnakeBody:
			while(positioned == False):
				if y > (item.GetY() + 2) or y < (item.GetX() - 2):
					if x > (item.GetX() + 2) or x < (item.GetX() - 2):
						positioned = True
				if positioned == False:
					x = random.randrange(0, 9)
					y = random.randrange(0, 9)
		for item in FoodList:
			while(positionedProper == False):
				if y > (item.GetY() + 1) or y < (item.GetY() - 1):
					if x > (item.GetX() + 1) or x < (item.GetX() - 1):
						positionedProper = True
				if positionedProper = False:
					x = random.randrange(0, 9)
					y = random.randrange(0, 9)
		FoodList.append(vector2(x, y))
					