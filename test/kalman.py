from magum import Magum
from array import *

DT = 0.02 # 20ms

axisOffset = array('i',[])

magum = Magum(250,1,2,1) # G_scaleRange = 250 | FsDouble = 1 (enabled) | A_scaleRange = 2  | lnoise = 1 (on)
i = 0

# first of all calibrate the sensors
axisOffset = magum.calibrateSens(1000)

while True:
	try:
		kFx = magum.kalmanFilter(DT,'x',axisOffset)
		kFy = magum.kalmanFilter(DT,'y',axisOffset)
		kFz = magum.kalmanFilter(DT,'z',axisOffset)
	except IOError:
		pass

	if i%20 == 0:
		print str(kFx) + ',' + str(kFy) + ',' + str(kFz)

	i += 1