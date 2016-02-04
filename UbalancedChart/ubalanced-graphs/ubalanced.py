from flask import Flask, render_template, jsonify
from magum import Magum
from array import *
import logging

app = Flask(__name__)
magum = Magum() # default configs
app.debug = False

log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

sensors = [
	{
		'id': 1,
		'name': 'Accelerometer'
	},
	{
		'id':2,
		'name':'Gyroscope'
	},
	{
		'id':3,
		'name':'Magnetometer'
	},
	{
		'id':4,
		'name':'Temperature'
	}
]

@app.route("/sensor/<int:sensor_id>",methods=['GET'])
def getSens(sensor_id):
	if sensor_id == 1:
		data = magum.readAData('gcomp')
		return str(data[0]) + ',' + str(data[1]) + ',' + str(data[2])
	elif sensor_id == 2:
		data = magum.readGData('rads')
		return str(data[0]) + ',' + str(data[1]) + ',' + str(data[2])
	elif sensor_id == 3:
		data = magum.readMData('ut')
		return str(data[0]) + ',' + str(data[1]) + ',' + str(data[2])
	elif sensor_id == 4:
		data = magum.readTData('C')
		return str(int(data))
	else:
		abort(404)
	
	

@app.route("/")
def main():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5001,host='0.0.0.0')