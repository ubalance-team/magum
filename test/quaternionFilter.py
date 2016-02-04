from magum import Magum 
import math
from array import *

def madgwickQuaternionFilter(aCompArray,gCompArray,mCompArray):
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

magum = Magum(250,0,2,1)
i = 0

ar = array('f',[])

while True:
	aCompArray = magum.readAData('gcomp')
	gCompArray = magum.readGData('rads')
	mCompArray = magum.readMData('ut')

	ar = madgwickQuaternionFilter(aCompArray,gCompArray,mCompArray)

	if i%20 == 0:
		print madgwickQuaternionFilter(aCompArray,gCompArray,mCompArray)
	i += 1