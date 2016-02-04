from magum import Magum
from array import *
import time
import math


# enable Gyro, Accelerometer and Magnetometer
magum = Magum(2000,0,2,1) # G_scaleRange = 2000 | FsDouble = 0 (disabled) | A_scaleRange = 2  | lnoise = 1 (on)
axisOffset = magum.calibrateSens(1000) # calibration (not necessary with read Data functions)

if axisOffset[0] >= 32768:
	axisOffset[0] -= 65536
if axisOffset[1] >= 32768:
	axisOffset[1] -= 65536
if axisOffset[2] >= 32768:
	axisOffset[2] -= 65536

aOffsetX = (axisOffset[0]/4) * 0.244
aOffsetY = (axisOffset[1]/4) * 0.244
aOffsetZ = (axisOffset[2]/4) * 0.244

aOffsetX2 = aOffsetX * aOffsetX 
aOffsetY2 = aOffsetY * aOffsetY
aOffsetZ2 = aOffsetZ * aOffsetZ

# getting angles
aOffsetX = math.atan(aOffsetX/math.sqrt(aOffsetY2+aOffsetZ2))*(180/math.pi)
aOffsetY = math.atan(aOffsetY/math.sqrt(aOffsetX2+aOffsetZ2))*(180/math.pi)
aOffsetZ = math.atan(aOffsetZ/math.sqrt(aOffsetX2+aOffsetY2))*(180/math.pi)


while True:
		axis = magum.readAData('deg')
		print str(axis[0]-aOffsetX) + ',' + str(axis[1]-aOffsetY) + ',' + str(axis[2]-aOffsetZ)
		time.sleep(.900)
