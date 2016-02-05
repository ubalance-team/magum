from __future__ import division
from array import *
import smbus
import time
import sys
import os
import shlex
import subprocess
import math
from .regs import *

# example list of registers
def _regsExample(sensor):
	if sensor == 'a':
		print "Error: wrong register supplied to setSensConf(sensor,reg,hexVal).\nUse one from the list instead:\n"
		for index,value in enumerate(A_CREGS_LIST):
			print value
		sys.exit(1)
	if sensor == 'm':
		print "Error: wrong register supplied to setSensConf(sensor,reg,hexVal).\nUse one from the list instead:\n"
		for index,value in enumerate(M_CREGS_LIST):
			print value
		sys.exit(1)
	if sensor == 'g':
		print "Error: wrong register supplied to setSensConf(sensor,reg,hexVal).\nUse one from the list instead:\n"
		for index,value in enumerate(G_CREGS_LIST):
			print value
		sys.exit(1)

# get correct value scale
def _dataConvertion(Object,sensor,axisList,uM=None):

	if sensor == 'a':
		currScale = Object.read_byte_data(I2C_AM_ADDRESS,A_XYZ_DATA_CFG)
		if currScale%4 == 0: # last two bits are setted to 0b00 (2g mode)
			# sensitivity = 4096
			factor = 1
		elif currScale%2 != 0 and (currScale+1)%4 != 0: # last two bits are setted to 0b01 (4g mode)
			# sensitivity = 2048
			factor = 2
		elif currScale%2 != 0 and (currScale+1)%4 == 0: # last two bits are setted to 0b11 (reserved)
			print 'Error: this bit configuration is reserved to the sensor'
			sys.exit(1)
		else: # last two bits are setted to 0b10 (8g mode)
			# sensitivity = 1024
			factor = 4

		if axisList[0] >= 32768:
			axisList[0] -= 65536
		if axisList[1] >= 32768:
			axisList[1] -= 65536
		if axisList[2] >= 32768:
			axisList[2] -= 65536

		x = ((axisList[0]/4) * 0.244 * factor)
		y = ((axisList[1]/4) * 0.244 * factor)
		z = ((axisList[2]/4) * 0.244 * factor)

		# raw values
		if uM in (None,'raw'):
			return axisList
		# g components
		elif uM == 'gcomp':
			axisList[0] = x/1000
			axisList[1] = y/1000
			axisList[2] = z/1000

			return axisList
		# degrees
		elif uM == 'deg':
			x2 = x * x
			y2 = y * y
			z2 = z * z

			axisList[0] = math.atan(x/math.sqrt(y2+z2))*(180/math.pi)
			axisList[1] = math.atan(y/math.sqrt(x2+z2))*(180/math.pi)*(-1)
			axisList[2] = math.atan(z/math.sqrt(x2+y2))*(180/math.pi)*(-1)

			return axisList

		elif uM == ('rad'):
			x2 = x * x
			y2 = y * y
			z2 = z * z

			axisList[0] = math.atan(x/math.sqrt(y2+z2))
			axisList[1] = math.atan(y/math.sqrt(x2+z2))*(-1)
			axisList[2] = math.atan(z/math.sqrt(x2+y2))*(-1)

			return axisList

		else:
			print 'Error: Invalid measure unit given to method _dataConvertion(Object,sensor,axisList,uM=None) for accelerometer'
			sys.exit(1)

	if sensor == 'm':
		sensitivity = 0.1
		if axisList[0] >= 32768:
			axisList[0] -= 65536
		if axisList[1] >= 32768:
			axisList[1] -= 65536
		if axisList[2] >= 32768:
			axisList[2] -= 65536
		if uM in (None,'raw'):
			return axisList

		elif uM == 'ut':
			axisList[0] = ((axisList[0])*sensitivity)
			axisList[1] = ((axisList[0])*sensitivity)
			axisList[2] = ((axisList[0])*sensitivity)
			return axisList


	if sensor == 'g':
		currScale = Object.read_byte_data(I2C_G_ADDRESS,G_CTRL_REG0)
		currRange = Object.read_byte_data(I2C_G_ADDRESS,G_CTRL_REG3)
		if currRange %2 == 1:
			ctrlDouble = 2
		else:
			ctrlDouble = 1	

		if axisList[0] >= 32769:
			axisList[0] = axisList[0] - 65535
		if axisList[1] >= 32769:
			axisList[1] = axisList[1] - 65535
		if axisList[2] >= 32769:				
			axisList[2] = axisList[2] - 65535

		if uM in (None,'raw'):
			return axisList
		elif uM in ('degs','rads'):
			if currScale%4 == 0: # last two bits are setted to 0b00 (+/- 2000/4000 mode)
				sensitivity = 62.5 * ctrlDouble / 1000
			elif currScale%2 != 0 and (currScale+1)%4 == 0: # last two bits are setted to 0b01 (+/- 1000/2000 mode)
				sensitivity = 31.25 * ctrlDouble / 1000
			elif currScale%2 != 0 and (currScale+1)%4 != 0: # last two bits are setted to 0b11 (+/- 250/500 mode)
				sensitivity = 7.8125 * ctrlDouble / 1000
			else: # last two bits are setted to 0b10 (+/- 500/1000 mode)
				sensitivity = 15.625 * ctrlDouble / 1000

			axisList[0] = -(axisList[0]*sensitivity)
			axisList[1] = -(axisList[1]*sensitivity)
			axisList[2] = (axisList[2]*sensitivity)

			if uM == ('rads'):
				axisList[0] = math.radians(axisList[0])
				axisList[1] = math.radians(axisList[1])
				axisList[2] = math.radians(axisList[2])

			return axisList

		else:
			print 'Error: Invalid measure unit given to method _dataConvertion(Object,sensor,axisList,uM=None) for gyroscope'
			

	else:
		print "Error: Incorrect parameters supplied to method _dataConvertion(Object,sensor,axisList,uM=None)"
		sys.exit(1)
