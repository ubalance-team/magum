from magum import Magum
from array import *
import time

# enable Gyro, Accelerometer and Magnetometer
magum = Magum(2000,0,2,1) # G_scaleRange = 2000 | FsDouble = 0 (disabled) | A_scaleRange = 2  | lnoise = 1 (on)

while True:
		axis = magum.readAData('deg')
		print str(axis[0]) + ',' + str(axis[1]) + ',' + str(axis[2])
		time.sleep(.900)
