window.onload = function () {

function upGraph(){


// initial values of dataPoints
var dps = [
{label: "Xaxis", y: 0},
{label: "Yaxis", y: 0},
{label: "Zaxis", y: 1}
];
var totalEmployees = " ";
var text = $.cookie('text');
var min = parseInt($.cookie('minValBar'));
var max = parseInt($.cookie('maxValBar'));

var chart = new CanvasJS.Chart("bar-accelerometer",{
	theme: "theme2",
	title:{ 
		text: text
	},
	axisY: {				
		title: "Axis value(" + $.cookie('uM') + ")",
		minimum: min,
		maximum: max
	},					
	legend:{
		verticalAlign: "top",
		horizontalAlign: "centre",
		fontSize: 18

	},
	data : [{
		type: "column",
		showInLegend: true,
		legendMarkerType: "none",				
		legendText: totalEmployees,
		indexLabel: "{y}" + $.cookie('uM'),
		dataPoints: dps
	}]
});

// renders initial chart
chart.render();

var updateInterval = 10;  // milliseconds

var updateChart = function () {

	$.get( "/sensor/" + $.cookie('sensor'), function(data) {
		res = data.split(',');
		dps[0].y = parseFloat(res[0]);
		dps[1].y = parseFloat(res[1]);
		dps[2].y = parseFloat(res[2]);
    });
	
	chart.render();

};
	// update chart after specified interval
	setInterval(function(){updateChart()}, updateInterval);
}
}