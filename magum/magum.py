
#!/usr/bin/python

"""
MAGUM python module (Beta 1.1.0)

MAGUM stands for (Magnetometer, Accelerometer and Gyroscope Udoo Management)
it includes some modules such as smbus, time, os, sys, subprocess etc.. to manage the udoo-neo 
motion sensors over the I2C serial communicaton protocol.

Because the I2C device interface is opened R/W using smbus module, 
users of this module usually MUST have ROOT permissions.

"""

# including necessary modules
import smbus
import time
import sys
import os
import shlex
import subprocess
import re
import math

from array import *
from .utils import _dataConvertion
from .utils import _regsExample
from .regs  import *

class Magum:
	""" Magum(gScaleRange,fsDouble,aScaleRange,noise) -> Magum
    Return a new Magum object that is (optionally) 
    automatically initialized with the default values. 
    """
	_i2cBus	= smbus.SMBus(3) # open communication to I2C channel 4
	_calibrated = False # check calibration
	accScale = None
	gyrScale = None
	gyrDouble = None
	# Complementary Filter Attributes
	compAux = 0
	_cFAngleX = 0
	_cFAngleY = 0
	_cFAngleZ = 0

	compAux = 0


	def __init__(self,gScaleRange=None,fsDouble=None,aScaleRange=None,noise=None):
		self.killDrivers(1)
		self._initAm(aScaleRange,noise)
		self._initG(gScaleRange,fsDouble)

	# accelerometer and magnetometer initialization 
	def _initAm(self,scaleRange=None,noise=None):
		self.toStandby('a')

		if noise == 1 and scaleRange in (2,4):
			regNoise = 0x0c
		elif noise in (0,None):
			regNoise = 0x00
		else:
			print 'Error: incorrect low noise value, it can assume 1 (enabled) or 0 (diabled)'
			sys.exit(1)

		if scaleRange == 2:
			self.setSensConf('a','A_XYZ_DATA_CFG',0x00) # set range to +/- 2g
		elif scaleRange == 4:
			self.setSensConf('a','A_XYZ_DATA_CFG',0x01) # set range to +/- 4g
		elif scaleRange == 8:
			self.setSensConf('a','A_XYZ_DATA_CFG',0x02) # set range to +/- 8g
		elif scaleRange == None:
			self._i2cBus.write_byte_data(I2C_AM_ADDRESS,A_CTRL_REG1,0x01)	# set to active mode
			time.sleep(.300)											    # sleep 300 ms
		else:
			print 'Error: incorrect aScalRange value, read the documentation for the correct config.'
			sys.exit(1)
		
		self.accScale = scaleRange

		self._i2cBus.write_byte_data(I2C_AM_ADDRESS,A_CTRL_REG1,0x01 | regNoise) # set to active mode
		time.sleep(.300) 										# sleep 300 ms

		self._i2cBus.write_byte_data(I2C_AM_ADDRESS,M_CTRL_REG1,0x03)	# enable both accelerometer and magnetometer sensors
													
	
	# gyroscope initialization 
	def _initG(self,scaleRange=None,fsDouble=None):
		self.toStandby('g')

		if fsDouble == 1:
			self.gyrDouble = 2
			self.setSensConf('g','G_CTRL_REG3',0x01)
		elif fsDouble == 0:
			self.gyrDouble = 1
			self.setSensConf('g','G_CTRL_REG3',0x00)
		else:
			self.gyrDouble = 1
			self.setSensConf('g','G_CTRL_REG3',0x00)
		
		if scaleRange == 2000:
			self.setSensConf('g','G_CTRL_REG0',0x00) # set range to +/- 2000dps (4000dps if CTRL_REG3 is set to double)
		elif scaleRange == 1000:
			self.setSensConf('g','G_CTRL_REG0',0x01) # set range to +/- 1000dps (2000dps if CTRL_REG3 is set to double)
		elif scaleRange == 500:
			self.setSensConf('g','G_CTRL_REG0',0x02) # set range to +/- 500dps (1000dps if CTRL_REG3 is set to double)
		elif scaleRange == 250:
			self.setSensConf('g','G_CTRL_REG0',0x03) # set range to +/- 250dps (500dps if CTRL_REG3 is set to double)
		elif scaleRange == None:
			self._i2cBus.write_byte_data(I2C_G_ADDRESS,A_CTRL_REG1,0x16)	# set to active mode
			time.sleep(.300)											    # sleep 300 ms
		else:
			print 'Error: incorrect gScalRange value, read the documentation for the corret config.'
			sys.exit(1)

		self.gyrScale = scaleRange

		self._i2cBus.write_byte_data(I2C_G_ADDRESS,G_CTRL_REG1,0x16) # set to active mode
		time.sleep(.300) 									         # sleep 300ms

	def toStandby(self,sensor):
		if sensor in ('a','m'):
			currReg = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_CTRL_REG1) # get current configuration
			if currReg % 2 == 1:
				self._i2cBus.write_byte_data(I2C_AM_ADDRESS,A_CTRL_REG1,currReg - 1) # set to standby_mode
		if sensor in ('g'):
			currReg = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_CTRL_REG1) # get old configuration
			currReg = currReg >> 2
			currReg = currReg << 2
			self._i2cBus.write_byte_data(I2C_G_ADDRESS,G_CTRL_REG1,currReg) # set to standby_mode

		time.sleep(.300) # sleep 300ms

	def toActive(self,sensor):
		if sensor in ('a','m'):
			currReg = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_CTRL_REG1) # get current configuration
			self._i2cBus.write_byte_data(I2C_AM_ADDRESS,A_CTRL_REG1,currReg) # set to active_mode
		if sensor in ('g'):
			currReg = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_CTRL_REG1) # get old configuration
			currReg = currReg >> 2
			currReg = currReg << 2
			currReg = currReg + 2

			self._i2cBus.write_byte_data(I2C_G_ADDRESS,G_CTRL_REG1,currReg) # set to active_mode
		time.sleep(.300) # sleep 300ms

	# enable/disable system drivers
	def killDrivers(self,x):
		proc1 = subprocess.Popen(shlex.split('lsmod'),stdout=subprocess.PIPE)
		proc2 = subprocess.Popen(shlex.split('grep fxas2100x'),stdin=proc1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
		out1,err1=proc2.communicate()

		proc1 = subprocess.Popen(shlex.split('lsmod'),stdout=subprocess.PIPE)
		proc2 = subprocess.Popen(shlex.split('grep fxos8700'),stdin=proc1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
		out2,err2=proc2.communicate()

		if x == 1:
			if out1:
				os.system('rmmod fxas2100x')
			if out2:
				os.system('rmmod fxos8700')
		elif x == 0:
			if not out1:
				os.system('modprobe fxas2100x')
			if not out2:
				os.system('modprobe fxos8700')
		else:
			print "Error: wrong killDrivers(x) parameter.\n self.killDrivers(0): enable drivers \n killDrivers(1): disable drivers."
			sys.exit(1)

	# sensor calibration 
	def calibrateSens(self,samples):
		acc_angle = array('i',[])
		rate_gyr = array('i',[])

		i = 0
		sumX = 0
		sumY = 0
		sumZ = 0

		gsumX = 0
		gsumY = 0
		gsumZ = 0

		tarXvect = array('i',[])
		tarYvect = array('i',[])
		tarZvect = array('i',[])

		gtarXvect = array('i',[])
		gtarYvect = array('i',[])
		gtarZvect = array('i',[])

		gyrXangle = 0.0
		gyrYangle = 0.0
		gyrZangle = 0.0

		accXangle = 0.0
		accYangle = 0.0
		accZangle = 0.0

		axisOffset = array('i',[])

		# sensors Calibration
		raw_input("CAUTION! Sensors calibration.\nSet your udoo-neo in an horizontal position and press Enter Key...\n")
		
		perc = -1
		while i<samples:
			acc_angle = self.readAData()
			rate_gyr = self.readGData()

			factor = self.accScale/2

			if acc_angle[0] >= 32768:
				tarXvect.insert(i,int(acc_angle[0]-65536))
			else:
				tarXvect.insert(i,int(acc_angle[0]))

			if acc_angle[1] >= 32768:
				tarYvect.insert(i,int(acc_angle[1]-65536))
			else:
				tarYvect.insert(i,int(acc_angle[1]))

			if acc_angle[2] >= 32768:
				tarZvect.insert(i,int(acc_angle[2] - 65536 + 16384/factor))
			else:
				tarZvect.insert(i,int(acc_angle[2] + 16384/factor))	

			if rate_gyr[0] >= 32768:
				gtarXvect.insert(i,int(rate_gyr[0]-65536))
			else:
				gtarXvect.insert(i,int(rate_gyr[0]))

			if rate_gyr[1] >= 32768:
				gtarYvect.insert(i,int(rate_gyr[1]-65536))
			else:
				gtarYvect.insert(i,int(rate_gyr[1]))

			if rate_gyr[2] >= 32768:
				gtarZvect.insert(i,int(rate_gyr[2] - 65536))
			else:
				gtarZvect.insert(i,int(rate_gyr[2]))

			sumX += tarXvect[i]
			sumY += tarYvect[i]
			sumZ += tarZvect[i]

			gsumX += gtarXvect[i]
			gsumY += gtarYvect[i]
			gsumZ += gtarZvect[i]

			loading = int((i*100)/samples)
			if loading != perc:
				print "Calibration percentage: " + str(int(loading)) + "%"
				perc = loading
			i += 1

		print "Calibration percentage: 100%\n"

		avgX = sumX/samples
		avgY = sumY/samples
		avgZ = sumZ/samples

		gavgX = gsumX/samples
		gavgY = gsumY/samples
		gavgZ = gsumZ/samples

		axisOffset.insert(0,avgX)
		axisOffset.insert(1,avgY)
		axisOffset.insert(2,avgZ)
		axisOffset.insert(3,gavgX)
		axisOffset.insert(4,gavgY)
		axisOffset.insert(5,gavgZ)

		self._calibrated = True
		return axisOffset

	# set sensors configurations
	def setSensConf(self,sensor,reg,hexVal):	
		self.toStandby(sensor)

		if sensor == 'a':
			if reg in A_CREGS_LIST:
				self._i2cBus.write_byte_data(I2C_AM_ADDRESS,COMPLETE_REGS_DICT[reg],hexVal)
			else:
				_regsExample('a')
		if sensor == 'm':
			if reg in M_CREGS_LIST:
				if bool(is_hex(str(hexVal))):
					self._i2cBus.write_byte_data(I2C_AM_ADDRESS,COMPLETE_REGS_DICT[reg],hexVal)
			else:
				_regsExample('m')
		if sensor == 'g':
			if reg in G_CREG_LIST:	
				self._i2cBus.write_byte_data(I2C_AM_ADDRESS,COMPLETE_REGS_DICT[reg],hexVal)
			else:
				_regsExample('g')
		time.sleep(.300) # sleep 300ms
		self.toActive(sensor)

	# read accelerometer data
	def readAData(self,uM=None):
		axisList = array('f',[])

		# getting x,y,z coordinate shifting first 8bit and adding 
		# (with the or operator) the others 8 bit to the address
		xMsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OUT_X_MSB)
		xLsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OUT_X_LSB)
		
		xRaw = (xMsbRaw << 8 | xLsbRaw) # x axis

		yMsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OUT_Y_MSB)
		yLsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OUT_Y_LSB)
		
		yRaw = (yMsbRaw << 8 | yLsbRaw) # y axis

		zMsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OUT_Z_MSB)
		zLsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OUT_Z_LSB)
		
		zRaw = (zMsbRaw << 8 | zLsbRaw) # z axis

		axisList.insert(0,xRaw)
		axisList.insert(1,yRaw)
		axisList.insert(2,zRaw)

		axisList = _dataConvertion(self._i2cBus,"a",axisList,uM)

		return axisList


	# read magnetometer data
	def readMData(self,uM=None):
		axisList = array('f',[])

		# getting x,y,z coordinate shifting first 8bit and adding 
		# (with the or operator) the others 8 bit to the address
		xMsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,M_OUT_X_MSB)
		xLsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,M_OUT_X_LSB)

		xRaw = xMsbRaw << 8 | xLsbRaw # x axis

		yMsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,M_OUT_Y_MSB)
		yLsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,M_OUT_Y_LSB)

		yRaw = yMsbRaw << 8 | yLsbRaw # y axis

		zMsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,M_OUT_Z_MSB)
		zLsbRaw = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,M_OUT_Z_LSB)

		zRaw = zMsbRaw << 8 | zLsbRaw # z axis

		axisList.insert(0,xRaw)
		axisList.insert(1,yRaw)
		axisList.insert(2,zRaw)

		axisList = _dataConvertion(self._i2cBus,'m',axisList,uM)

		return axisList

	# read gyroscope data
	def readGData(self,uM=None):
		axisList = array('f',[])
		# getting x,y,z coordinate shifting first 8bit and adding 
		# (with the or operator) the others 8 bit to the address
		xMsbRaw = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_OUT_X_MSB)
		xLsbRaw = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_OUT_X_LSB)

		xRaw = xMsbRaw << 8 | xLsbRaw # x axis

		yMsbRaw = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_OUT_Y_MSB)
		yLsbRaw = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_OUT_Y_LSB)

		yRaw = yMsbRaw << 8 | yLsbRaw # y axis

		zMsbRaw = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_OUT_Z_MSB)
		zLsbRaw = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_OUT_Z_LSB)

		zRaw = zMsbRaw << 8 | zLsbRaw # z axis

		axisList.insert(0,xRaw)
		axisList.insert(1,yRaw)
		axisList.insert(2,zRaw)

		axisList = _dataConvertion(self._i2cBus,"g",axisList,uM)

		return axisList

	def readTData(self,uM=None):
		tempRaw= self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_TEMP)

		if tempRaw >= 128:
			tempCels= float((tempRaw-256)*0.96)
		else:
			tempCels=float((tempRaw)*0.96)
			
		if uM in (None, 'raw'):
			return tempRaw
		if uM == 'C':
			return tempCels
		if uM == 'K':
			tempKelv= float(tempCels + 273.15)
			return tempKelv
		if uM == 'F':
			tempFahr= float(float(tempCels * 1.8)+32)
			return tempFahr

	# complementary filter algorithm
	def compFilter(self,DT,axisOffset):
		exTime = 0.013 # execution time
		if DT < exTime:
			print "Error: DT is too small to sample the accelerometer and gyroscope data.\nDT must be greater than 0.013."
			sys.exit(1)
		else:
			if self._calibrated == True:
				highPass = DT / (DT + exTime)
				rate_gyr = array('i',[])
				acc_angle = array('i',[])

				cFAngleAxis = array('f',[])

				rate_gyr = self.readGData()
				acc_angle = self.readAData()

				factor = self.accScale/2

				gFactor = float((self.gyrScale/(1000*32))*self.gyrDouble)

				if acc_angle[0] >= 32768:
					acc_angle[0] -= 65536
				if acc_angle[1] >= 32768:
					acc_angle[1] -= 65536
				if acc_angle[2] >= 32768:
					acc_angle[2] -= 65536

				if rate_gyr[0] >= 32768:
					rate_gyr[0] -= 65536
				if rate_gyr[1] >= 32768:
					rate_gyr[1] -= 65536
				if rate_gyr[2] >= 32768:
					rate_gyr[2] -= 65536

				x = (((acc_angle[0] - axisOffset[0])/4) * 0.244 * factor)
				y = (((acc_angle[1] - axisOffset[1])/4) * 0.244 * factor)
				z = (((acc_angle[2] - axisOffset[2])/4) * 0.244 * factor)

				x2 = x * x
				y2 = y * y
				z2 = z * z

				accXangle = math.atan(x/math.sqrt(y2+z2))*(180/math.pi)
				accYangle = math.atan(y/math.sqrt(x2+z2))*(180/math.pi)
				accZangle = math.atan(z/math.sqrt(x2+y2))*(180/math.pi)

				gyrXangle = float(((rate_gyr[0] - axisOffset[3]) * gFactor)/DT)
				gyrYangle = float(((rate_gyr[1] - axisOffset[4]) * gFactor)/DT)
				gyrZangle = float(((rate_gyr[2] - axisOffset[5]) * gFactor)/DT)

				modGyr = (gyrXangle*gyrXangle) + (gyrYangle*gyrYangle) + (gyrZangle*gyrZangle)

				# Only for the first time we get the position or if the base doesn't move
				#if self.compAux == 0 || (math.fabs(gyrXangle) <= 5 && math.fabs(gyrYangle) <= 5 && math.fabs(gyrZangle) <= 5):
				if self.compAux == 0:
					self._cFAngleX = float(accXangle)
					self._cFAngleY = float(accYangle)
					self._cFAngleZ = float(accZangle)
					self.compAux = 1
				else:													# Then we use the Complementary Filter
					self._cFAngleX = (highPass) * (self._cFAngleX + gyrXangle * DT) + (1-highPass)*(accXangle)
					self._cFAngleY = (highPass) * (self._cFAngleY + gyrYangle * DT) + (1-highPass)*(accYangle)
					self._cFAngleZ = (highPass) * (self._cFAngleZ + gyrZangle * DT) + (1-highPass)*(accZangle)

				cFAngleAxis.insert(0,self._cFAngleX)
				cFAngleAxis.insert(1,self._cFAngleY*(-1))
				cFAngleAxis.insert(2,self._cFAngleZ*(-1))

				gyrXangle = float((rate_gyr[0] - axisOffset[3]) * gFactor)
				gyrYangle = float((rate_gyr[1] - axisOffset[4]) * gFactor)
				gyrZangle = float((rate_gyr[2] - axisOffset[5]) * gFactor)

				if compAux == 0:					# Only for the first time we get the position
					cFAnglex = float(accXangle)
					cFAngleY = float(accYangle)
					cFAngleZ = float(accZangle)
					compAux = 1
				else:								# Then we use the Complementary Filter
					cFAngleX = (highPass) * (cFAngleX + gyrXangle * DT) + (1-highPass)*(accXangle)
					cFAngleY = (highPass) * (cFAngleY + gyrYangle * DT) + (1-highPass)*(accYangle)
					cFAngleZ = (highPass) * (cFAngleZ + gyrZangle * DT) + (1-highPass)*(accZangle)

				cFAngleAxis.insert(0,cFAngleX)
				cFAngleAxis.insert(1,cFAngleY*(-1))
				cFAngleAxis.insert(2,cFAngleZ*(-1))
				
				time.sleep(DT-exTime)

				return cFAngleAxis

			else:
				print "Error: failed calibration.\nMake sure to calibrate the sensors using calibrateSens(sensor,samples)"
				sys.exit(1)
			
	
	# Kalman Filter
	# Note: this algorithm is under development, it may not work properly like a common Kalman Filter
	# If you want to improve this algorithm join us on github at https://github.com/ubalance-team/magum
	def kalmanFilter(self,DT,axis,axisOffset):
		exTime = 0.012 # execution time
		if DT < exTime:
			print "Error: DT is too small to sample the accelerometer and gyroscope data.\nDT must be greater than 0.015."
			sys.exit(1)
		else:
			if self._calibrated == True:
				rate_gyr = self.readGData()
				acc_angle = self.readAData()

				factor = self.accScale/2

				gFactor = float((self.gyrScale/(1000*32))*self.gyrDouble)

				if acc_angle[0] >= 32768:
					acc_angle[0] -= 65536
				if acc_angle[1] >= 32768:
					acc_angle[1] -= 65536
				if acc_angle[2] >= 32768:
					acc_angle[2] -= 65536

				if rate_gyr[0] >= 32768:
					rate_gyr[0] -= 65536
				if rate_gyr[1] >= 32768:
					rate_gyr[1] -= 65536
				if rate_gyr[2] >= 32768:
					rate_gyr[2] -= 65536

				x = (((acc_angle[0] - axisOffset[0])/4) * 0.244 * factor)
				y = (((acc_angle[1] - axisOffset[1])/4) * 0.244 * factor)
				z = (((acc_angle[2] - axisOffset[2])/4) * 0.244 * factor)
				
				x2 = x * x
				y2 = y * y
				z2 = z * z
				
				if axis == 'x':
					accAngle = math.atan(x/math.sqrt(y2+z2))*(180/math.pi)
					gyroRate = float((rate_gyr[0] - axisOffset[3]) * gFactor)
				elif axis == 'y':
					accAngle = math.atan(y/math.sqrt(x2+z2))*(180/math.pi)*(-1)
					gyroRate = float((rate_gyr[1] - axisOffset[4]) * gFactor)
				elif axis == 'z':
					accAngle = math.atan(z/math.sqrt(x2+y2))*(180/math.pi)*(-1)
					gyroRate = float((rate_gyr[2] - axisOffset[5]) * gFactor)

				Q_angle = 0.01
				Q_gyro = 0.0003
				R_angle = 0.01
				a_bias = 0

				AP_00 = 0
				AP_01 = 0
				AP_10 = 0
				AP_11 = 0

				KFangle = 0.0

				KFangle += DT * (gyroRate - a_bias)

				AP_00 += - DT * (AP_10 + AP_01) + Q_angle * DT
			  	AP_01 += - DT * AP_11
			  	AP_10 += - DT * AP_11
			  	AP_11 += + Q_gyro * DT
			 
			 	a = accAngle - KFangle

			  	S = AP_00 + R_angle
			  	K_0 = AP_00 / S
			  	K_1 = AP_10 / S
			 
			  	KFangle +=  K_0 * a
			  	a_bias  +=  K_1 * a
			  	AP_00 -= K_0 * AP_00
			  	AP_01 -= K_0 * AP_01
			  	AP_10 -= K_1 * AP_00
			  	AP_11 -= K_1 * AP_01
			 
			 	time.sleep(DT-exTime)

			  	return KFangle*float(180/math.pi)*0.9

			else:
				print "Error: failed calibration.\nMake sure to calibrate the sensors using calibrateSens(sensor,samples)"
				sys.exit(1)

	# Implementation of Sebastian Madgwick's "...efficient orientation filter for... inertial/magnetic sensor arrays"
	# (see http://www.x-io.co.uk/category/open-source/ for examples and more details)
	# which fuses acceleration, rotation rate, and magnetic moments to produce a quaternion-based estimate of absolute
	# device orientation
	def madgwickQuaternionFilter(self,aCompArray,gCompArray,mCompArray):
		ax = aCompArray[0]
		ay = aCompArray[1]
		az = aCompArray[2]

		mx = mCompArray[0]
		my = mCompArray[1]
		mz = mCompArray[2]

		gx = gCompArray[0]
		gy = gCompArray[1]
		gz = gCompArray[2]

		deltat = 0.001
		gyroMeasError =  math.pi * (5.0 / 180.0)
		gyroMeasDrift =  math.pi * (0.2 / 180.0)

		beta = math.sqrt(3.0 / 4.0) * gyroMeasError
		zeta = math.sqrt(3.0 / 4.0) * gyroMeasDrift

		q = array('f',[])

		q1 = 1.0
		q2 = 0.0
		q3 = 0.0
		q4 = 0.0
		norm = 0.0
		hx = 0.0
		hy = 0.0
		_2bx = 0.0
		_2bz = 0.0
		s1 = 0.0
		s2 = 0.0
		s3 = 0.0
		s4 = 0.0
		qDot1 = 0.0
		qDot2 = 0.0
		qDot3 = 0.0
		qDot4 = 0.0

		# Auxiliary variables to avoid repeated arithmetic
		_2q1mx = 0.0
		_2q1my = 0.0
		_2q1mz = 0.0
		_2q2mx = 0.0
		_4bx = 0.0
		_4bz = 0.0
		_2q1 = 2.0 * q1
		_2q2 = 2.0 * q2
		_2q3 = 2.0 * q3
		_2q4 = 2.0 * q4
		_2q1q3 = 2.0 * q1 * q3
		_2q3q4 = 2.0 * q3 * q4
		q1q1 = q1 * q1
		q1q2 = q1 * q2
		q1q3 = q1 * q3
		q1q4 = q1 * q4
		q2q2 = q2 * q2
		q2q3 = q2 * q3
		q2q4 = q2 * q4
		q3q3 = q3 * q3
		q3q4 = q3 * q4
		q4q4 = q4 * q4

		# Normalize accelerometer measurement
		norm = math.sqrt(ax * ax + ay * ay + az * az)
		if norm == 0.0: return # handle NaN
		norm = 1.0/norm
		ax *= norm
		ay *= norm
		az *= norm

		# Normalize magnetometer measurement
		norm = math.sqrt(mx * mx + my * my + mz * mz)
		if norm == 0.0: return # handle NaN
		norm = 1.0/norm
		mx *= norm
		my *= norm
		mz *= norm

		# Reference direction of Earth s magnetic field
		_2q1mx = 2.0 * q1 * mx
		_2q1my = 2.0 * q1 * my
		_2q1mz = 2.0 * q1 * mz
		_2q2mx = 2.0 * q2 * mx
		hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 + _2q2 * my * q3 + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4
		hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * q3 - my * q2q2 + my * q3q3 + _2q3 * mz * q4 - my * q4q4
		_2bx = math.sqrt(hx * hx + hy * hy)
		_2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * q4 - mz * q2q2 + _2q3 * my * q4 - mz * q3q3 + mz * q4q4
		_4bx = 2.0 * _2bx
		_4bz = 2.0 * _2bz

		# Gradient decent algorithm corrective step
		s1 = -_2q3 * (2.0 * q2q4 - _2q1q3 - ax) + _2q2 * (2.0 * q1q2 + _2q3q4 - ay) - _2bz * q3 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q3 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
		s2 = _2q4 * (2.0 * q2q4 - _2q1q3 - ax) + _2q1 * (2.0 * q1q2 + _2q3q4 - ay) - 4.0 * q2 * (1.0 - 2.0 * q2q2 - 2.0 * q3q3 - az) + _2bz * q4 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
		s3 = -_2q1 * (2.0 * q2q4 - _2q1q3 - ax) + _2q4 * (2.0 * q1q2 + _2q3q4 - ay) - 4.0 * q3 * (1.0 - 2.0 * q2q2 - 2.0 * q3q3 - az) + (-_4bx * q3 - _2bz * q1) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q2 + _2bz * q4) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q1 - _4bz * q3) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
		s4 = _2q2 * (2.0 * q2q4 - _2q1q3 - ax) + _2q3 * (2.0 * q1q2 + _2q3q4 - ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q2 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
		norm = math.sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4)  # normalize step magnitude
		norm = 1.0/norm
		s1 *= norm
		s2 *= norm
		s3 *= norm
		s4 *= norm

		# Compute rate of change of quaternion
		qDot1 = 0.5 * (-q2 * gx - q3 * gy - q4 * gz) - beta * s1
		qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy) - beta * s2
		qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx) - beta * s3
		qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx) - beta * s4

		# Integrate to yield quaternion
		q1 += qDot1 * deltat
		q2 += qDot2 * deltat
		q3 += qDot3 * deltat
		q4 += qDot4 * deltat
		norm = math.sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4) # normalize quaternion
		norm = 1.0/norm

		q.insert(0,q1 * norm)
		q.insert(1,q2 * norm)
		q.insert(2,q3 * norm)
		q.insert(3,q4 * norm)

		return q


	# get current sensors configurtaions
	def getCurrentConf(self,sensor,screen = None):

		if sensor == 'a':
			config = [None] * 28
			_regName = ['A_TRIG_CFG','A_CTRL_REG1','A_CTRL_REG2','A_CTRL_REG3','A_CTRL_REG4','A_CTRL_REG5','A_ASPL_COUNT','A_F_SETUP','A_XYZ_DATA_CFG','A_HP_FILTER_CUTOFF','A_PL_CFG',
					    'A_PL_COUNT','A_PL_BF_ZCOMP','A_PL_THS_REG','A_FFMT_CFG','A_FFMT_THS','A_FFMT_COUNT','A_VECM_CFG','A_VECM_THS_MSB','A_TRANSIENT_CFG',
					    'A_TRANSIENT_THS','A_TRANSIENT_COUNT','A_PULSE_CFG','A_PULSE_TMLT','A_PULSE_LTCY','A_OFF_X','A_OFF_Y','A_OFF_Z']
			config[0]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_TRIG_CFG)
			config[1]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_CTRL_REG1)
			config[2]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_CTRL_REG2)
			config[3]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_CTRL_REG3)
			config[4]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_CTRL_REG4)
			config[5]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_CTRL_REG5)
			config[6]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_ASPL_COUNT)
			config[7]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_F_SETUP)
			config[8]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_XYZ_DATA_CFG)
			config[9]  = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_HP_FILTER_CUTOFF)
			config[10] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_PL_CFG)
			config[11] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_PL_COUNT)
			config[12] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_PL_BF_ZCOMP)
			config[13] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_PL_THS_REG)
			config[14] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_FFMT_CFG)
			config[15] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_FFMT_THS)
			config[16] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_FFMT_COUNT)
			config[17] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_VECM_CFG)
			config[18] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_VECM_THS_MSB)
			config[19] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_TRANSIENT_CFG)
			config[20] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_TRANSIENT_THS)
			config[21] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_TRANSIENT_COUNT)
			config[22] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_PULSE_CFG)
			config[23] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_PULSE_TMLT)
			config[24] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_PULSE_LTCY)
			config[25] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OFF_X)
			config[26] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OFF_Y)
			config[27] = self._i2cBus.read_byte_data(I2C_AM_ADDRESS,A_OFF_Z)

		if sensor == 'm':
			config = [None] * 15
			_regName = ['M_OFF_X_MSB','M_OFF_X_LSB','M_OFF_Y_MSB','M_OFF_Y_LSB','M_OFF_Z_MSB','M_OFF_Z_LSB','M_THS_CFG','M_THS_COUNT',
					   'M_CTRL_REG1','M_CTRL_REG2','M_CTRL_REG3','M_VECM_CFG','M_VECM_THS_MSB','M_VECM_THS_LSB','M_VECM_CNT']
			config[0]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_OFF_X_MSB)
			config[1]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_OFF_X_LSB)
			config[2]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_OFF_Y_MSB)
			config[3]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_OFF_Y_LSB)
			config[4]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_OFF_Z_MSB)
			config[5]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_OFF_Z_LSB)
			config[6]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_THS_CFG)
			config[7]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_THS_COUNT)
			config[8]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_CTRL_REG1)
			config[9]  = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_CTRL_REG2)
			config[10] = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_CTRL_REG3)
			config[11] = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_VECM_CFG)
			config[12] = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_VECM_THS_MSB)
			config[13] = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_VECM_THS_LSB)
			config[14] = self._i2cBus.read_byte_data (I2C_AM_ADDRESS,M_VECM_CNT)
		
		if sensor == 'g':
			config = [None] * 8
			_regName = ['G_F_SETUP','G_CTRL_REG0','G_RT_CFG','G_RT_THS','G_RT_COUNT','G_CTRL_REG1','G_CTRL_REG2','G_CTRL_REG3']
			config[0]  = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_F_SETUP)
			config[1]  = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_CTRL_REG0)
			config[2]  = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_RT_CFG)
			config[3]  = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_RT_THS)
			config[4]  = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_RT_COUNT)
			config[5]  = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_CTRL_REG1)
			config[6]  = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_CTRL_REG2)
			config[7]  = self._i2cBus.read_byte_data(I2C_G_ADDRESS,G_CTRL_REG3)

		if screen == 1:
			for i,reg in enumerate(_regName):
				print reg + ': ' + str('0x{:02x}'.format(config[i]))

		return config
