from magum import Magum
from array import *

DT = 0.02 # 20ms

axisOffset = array('i',[])
i = 0
magum = Magum(250,1,2,1)

# first of all calibrate the sensor
axisOffset = magum.calibrateSens(1000)

while True:
	try:
		cFAngleAxis = magum.compFilter(DT,axisOffset) # Note: it might need a small time amount to get up to speed
	except IOError: #  avoid timeout errors
		pass

	if i%20 == 0:
		print str(int(round(cFAngleAxis[0],0))) + ',' + str(int(round(cFAngleAxis[1],0))) + ',' + str(int(round(cFAngleAxis[2],0)))

	i += 1
	# it's better to use % operator for printing out data, 
	# time.sleep may cause uncorrect data do to sampling operation