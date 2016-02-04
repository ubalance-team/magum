![magum_header](http://s11.postimg.org/6df3q6m2r/magum_header.png "Welcome to magum")


**Magnetometer, Accelerometer and Gyroscope UDOO Management (FXAS21002C, FXOS8700CQ)**


![licence](https://img.shields.io/badge/licence-GPLv2-blue.svg)
![python](https://img.shields.io/badge/implementation-python%202.7-green.svg)
![linux](https://img.shields.io/badge/platform-linux-orange.svg)
![udoo](https://img.shields.io/badge/platform-UDOO%20Neo-EC008C.svg)


For full documentation visit our [Site](https://www.magum.ml).

This Python module has been created to manage the sensors on the main board computer UDOO Neo. We tested magum on UDOO Neo rev. D with UDOObuntu RC1

# Table of contents
* [Introduction](#introduction)
    - [The sensors](#the-sensors)
    - [With Magum you can](#with-magum-you-can)
    - [Axis orientation](#axis-orientation)
    - [Bug reporting](#bug-reporting)
    - [Development](#development)
* [Getting Started](#getting-started)
* [Installation](#installation)
* [Usage](#usage)
    - [Initializing Magum](#initializing-magum)
    - [toStandby](#tostandby)
    - [toActive](#toactive)
    - [killDrivers](#killdrivers)
    - [setSensConf](#setsensconf)
    - [readAData](#readadata)
    - [readMData](#readmdata)
    - [readGData](#readgdata)
    - [readTData](#readtdata)
    - [getCurrentConf](#getcurrentconf)
    - [calibrateSens](#calibratesens)
    - [compFilter](#complementaryfilter)
    - [kalmanFilter](#kalmanfilter)
    - [madgwickQuaternionFilter](#madgwickQuaternionFilter)
* [UbalancedGraphs](#ubalancedgraphs)
* [Authors](#authors) 
* [Copyright](#copyright)


# Introduction <a name="introduction"></a>

##The sensors <a name="the-sensors"></a>

Below you can find a complete list of all sensors:

* **Gyroscope:** FXAS2100C from Freescale Semiconductor Inc. [(datasheet)](http://magum.altervista.org/datasheets/FXAS21002C.pdf) 

* **Accelerometer and Magnetometer:** FXOS8700CQ from Freescale Semiconductor Inc. [(datasheet)](http://magum.altervista.org/datasheets/FXOS8700CQ.pdf) 

##With Magum you can: <a name="with-magum-you-can"></a>

* get data from all registers and write on them too
* monitor in real time the values obtained by the sensors
* using algorithms that use both accelerometer and gyroscope to detect orientation, and magnetometer to measure magnetic fields

##Axis orientation<a name="axis-orientation"></a>

magum works with this axis orientation even if the accelerometer is below the board:

![axis_orientation](http://s14.postimg.org/6v8ihdtrl/assi2_small.png {width=120px height=160px})

## Bug reporting <a name="bug-reporting"></a>

To submit a bugreport use the GitHub bugtracker, opening an issue for the project:

[Open an issue](https://github.com/ubalance-team/magum/issues)

## Development <a name="development"></a>

You can get the latest version from the repository hosted at [GitHub](https://github.com/ubalance-team/magum)

The file [regs.py](https://github.com/ubalance-team/magum/magum/regs.py) contains the entire list of the registers from both sensors used by magum


# Getting Started <a name="getting-started"></a>

Magum works through the Python module [smbus-cffi from bivab](https://github.com/bivab/smbus-cffi) so you need a few things before you start:


* a C compiler (e.g. gcc)
* i2c developement header files server.
* [cffi](https://pypi.python.org/pypi/cffi/)
* PyPy or CPython development headers
* libffi-dev

To install these, you have to run the following commands from your terminal:

For Debian based distributions (e.g. Ubuntu distros, Linux Mint):

```bash 
sudo apt-get install build-essential libi2c-dev i2c-tools python-dev libffi-dev
``` 

For Arch Linux:

```bash 
pacman -S base-devel
pacman -S i2c-tools
```

Finally install cffi and smbus-cffi using pip with this command, or from the Github sources: [cffi](https://github.com/cffi/cffi), [smbus-cffi](https://github.com/bivab/smbus-cffi)

```bash 
pip install cffi
pip install smbus-cffi
```
# Installation <a name="installation"></a>

You can obtain magum in different ways:

* [Download](https://github.com/ubalance-team/magum/archive/master.zip>) the repository as zip and unpack it
* Clone our [Github repository](https://github.com/ubalance-team/magum) with this  command from terminal (you have to install git to do this)
```bash
sudo apt-get install git
git clone https://github.com/ubalance-team/magum.git
```
Now navigate in the folder where you (or git) downloaded the repository with the terminal and run this command: 
```bash
python setup.py install
```
Magum is now installed like any other Python modules already on your computer

# Usage <a name="usage"></a>

Here you can find a guide to getting used of the most important methods of magum

## Initializing magum <a name="initializing-magum"></a>

Magum is a Python class that you can initialize using parameters for configuring sensors

**Magum(gScaleRange,fsDouble,aScaleRange,noise)**

**NOTE:** If no parameters are entered the class will be automatically initialized with the last register configuration.

### Parameters

* **gScaleRange :** represents the range of the gyroscope. It can assume the following values: 250,500,1000,2000 dps.
* **fsDouble:** enables (with value 1) or disables (with value 0) the fsdouble function to double the scale range of the gyroscope
* **aScaleRange :** represents the range of the accelerometer. In can assume 2 for +/- 2g, 4 for +/- 4g or 8 for +/- 8g
* **noise :** enables (with value 1) or disables (with value 0) the lnoise function for the accelerometer sensor  

### Example

```python
magum = Magum(2000,0,2,1)
```

Creates an instance of Magum called magum with 2000dps of range for the gyroscope, fsdouble disabled, +/- 2g of range for the acceleremoter and lnoise function enabled.

##toStandby(sensor) <a name="tostandby"></a>

Put in standby mode the selected sensor

### Parameters

* **sensor :** type 'a' for accelerometer, 'm' for magnetometer, 'g' for gyroscope

### Example:

```python
magum.toStandby('a')
```

## toActive(sensor) <a name="toactive"></a>

Actives the selected sensor

###Parameters:

* **sensor :** type 'a' for accelerometer, 'm' for magnetometer, 'g' for gyroscope

### Example:

```python
  magum.toActive('a')
```

## killDrivers(x) <a name="killdrivers"></a>

Magum can not work if the system drivers of the sensors are managing them. So it is crucial disable them before starting (Magum does automatically when the instance is initialized). killDrivers disable or re-enable these drivers.

### Parameters:

* **x :** if 1 disables drivers, if 0 re-enables them

### Example:

```python
  magum.killDrivers(1) 
```

## setSensConf(sensor,reg,hexVal) <a name="setsensconf"></a>

With this method you can configure all the registers (contained in [regs.py](https://github.com/ubalance-team/magum/blob/master/regs.py))needed by the sensors. 

### Parameters:

* **sensor :** type 'a' for accelerometer, 'm' for magnetometer, 'g' for gyroscope
* **reg :** type a register name from [regs.py](https://github.com/ubalance-team/magum/blob/master/regs.py) list
* **hexValue :** type the hexadecimal value that you want to write in the chosen register 

### Example:

```python
  magum.setSensConf('a','A_XYZ_DATA_CFG',0x00)
```
  
Writes the value 0x00 value in the register named A_XYZ_DATA_CFG of the accelerometer 

## readAData(uM) <a name="readadata"></a>

With this method you can get data from accelerometer specifying the unit of measure. 
Returns an array of three elements:

* **array[0]** x axis
* **array[1]** y axis
* **array[2]** z axis

### Parameters:

* **uM :** type 'raw' for raw values, 'deg' for degrees, 'rad' for radiant, or 'gcomp' for components along the axes of the gravitational acceleration

**NOTE:** if no parameters are entered readAData returns raw values

### Example:

```python
array = magum.readAData('gcomp')
```

## readMData(uM) <a name="readmdata"></a>

With this method you can get data from magnetometer specifying the unit of measure
Returns an array of three elements:

* **array[0]** x axis
* **array[1]** y axis
* **array[2]** z axis

### Parameters:

* **uM :** type 'raw' for raw values, 'ut' for μT values

**NOTE:** if no parameters are entered readMData returns raw values

### Example:

```python
array = magum.readMData('ut')
```

## readGData(uM) <a name="readgdata"></a>

With this method you can get data from gyroscope specifying the unit of measure.
Returns an array of three elements:

* **array[0]** x axis
* **array[1]** y axis
* **array[2]** z axis

### Parameters:

* **uM :** type 'raw' for raw values, 'deg' for degrees or 'rad' for radiant

**NOTE:** if no parameters are entered readGData returns raw values

### Example:

```python
array = magum.readGData('rad')
```

## readTData(uM) <a name="readtdata"></a>
With this method you can get data from temperature sensor specifying the unit of measure.
Returns the value of temperature:

### Parameters:

* **uM :** type 'raw' for raw values, 'C' for Celsius degrees or 'K' for Kelvin, 'F' for Fahrenheit degrees

**NOTE:** if no parameters are entered readGData returns raw values

### Example:

```python
temp = magum.readTData('C')
```


## getCurrentConf(sensor,screen) <a name="getcurrentconf"></a>

This method returns the content of the registers of the selected sensor

### Parameters:

* **sensor :** type 'a' for accelerometer, 'm' for magnetometer, 'g' for gyroscope
* **screen :** type 1 if you want to print the values on screen or 0 if you don't

**NOTE:** if screen parameter is not specified, getCurrentConf will not print values on screen

### Example:

```python
magum.getCurrentConf('a',1)
```

## calibrateSens(samples) <a name="calibratesens"></a>

This method calibrates the sensors calculating an average based on a selected number of samples (we suggest to work with 1000 samples).
Returns an array of 9 elements, with the offsets that you have to subtract from sensors values:

* **indexes from 0 to 2:** accelerometer
* **indexes from 3 to 5:** gyroscope
* **indexes from 6 to 8:** magnetometer  

### Parameters:

* **samples :** type the number of samples to base the average for the calibration

### Example:

```python
array = magum.calibrateSens(1000)
```

## compFilter(DT,AxisOffset) <a name="complementaryfilter"></a>
Integrates the values from accelerometer and gyroscope using a complementary filter. This filter returns more accurate measurements and less noise. Returns an array with the angles values, for the x,y,z axes. 

### Parameters:

* **DT:** is the sampling interval
* **AxisOffset:** is the array with the offsets returned by calibrateSens(samples) method. It uses the first 6 values of this array

### Example:

```python
 angles_array = magum.compFilter(0.02,AxisOffset)
```

## kalmanFilter(DT,AxisOffset) <a name="kalmanfilter"></a>
Integrates the values from accelerometer and gyroscope using Kalman filter. This filter is more accurate than complementary filter but requires more computational power. Return the inclination angle from the selected axis.  

### Parameters:
* **DT:** is the sampling interval
* **axis:** type the desidered axis: 'x', 'y' or 'z'
* **axisOffset:** is the array with the offsets returned by calibrateSens(samples) method.

### Example:
```python
x_angle = magum.kalmanFilter(0.02,'x',AxisOffset)
y_angle = magum.kalmanFilter(0.02,'y',AxisOffset)
```

## madgwickQuaternionFilter(aCompArray,gCompArray,mCompArray) <a name="madgwickQuaternionFilter"></a>
Implementation of Sebastian Madgwick's algorithm, wich fuses acceleration, rotation rate and magnetic moments to produce a quaternion-based estimate of absolute device orientation. Return an array filled with quaternions (q1, q2, q3,q4)

### Parameters:
* **aCompArray:** array of accelerometer g-components axis values 
* **gCompArray:** array of gyroscope axis values in rad/s
* **mCompArray:** array of magnetometer axis values in μT

### Example:

```python
qArray= magum.madgwickQuaternionFilter(aCompArray,gCompArray,mCompArray)
```

#UbalancedGraphs

![ubalnced_graphs](http://s16.postimg.org/8cweat8gl/graphs_header.jpg)

In order to use UbalancedGraphs web application, you should install Frask framework. To do this you can run from terminal the following command: 

```bash
pip install Flask
```

To install Ubalanced graphs application, move to the main directory that you've cloned from remote magum repository, then move to the /UbalancedGraphs directory and run (as root):

```bash
sudo python setup.py
```

To start ubalanced graphs web app start the server as a service from terminal typing (make sure you are running as root):

```bash
sudo service ubalanced start
```

Now, you can access to UbalancedGraphs web application from your favourite browser at this address (assuming you are connected to UDOO via USB): [192.168.7.2:5001](http://192.168.7.2)

To stop the service just type:

```bash
sudo service ubalanced stop
```

#Authors <a name="authors"></a>


| Name               | Twitter    	      |
|:-------------------|:-------------------|
| Francesco Guerri   |[![g_tweet][1l]][2l]|
| Francesco Orlandi  |[![o_tweet][1l]][3l]|
| Umberto Cucini     |[![c_tweet][1l]][4l]|


[1l]: http://s15.postimg.org/dj8qlfb2v/tweetbutton.png)
[2l]: https://twitter.com/rirri93
[3l]: https://twitter.com/0rla3
[4l]: https://twitter.com/umbertocucini

#Copyright <a name="copyright"></a>

Magum is under GPL licence. See [LICENSE](https://github.com/ubalance-team/magum/blob/master/LICENSE) file for the complete documentation
















