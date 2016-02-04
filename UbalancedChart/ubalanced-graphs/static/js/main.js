var config1 = liquidFillGaugeDefaultSettings();
var config2 = liquidFillGaugeDefaultSettings()
config2.minValue = 0;
config2.maxValue = 40;
config2.circleColor = "#178BCA";
config2.textColor = "#fff";
config2.waveTextColor = "#fff";
config2.waveColor = 'rgba(23,139,202,0.5)';
config2.circleThickness = 0.2;
config2.textVertPosition = 0.2;
config2.waveAnimateTime = 1000;
config2.minus = true;

config1.minValue = 0
config1.maxValue = 100
config1.circleColor = "#FF7777";
config1.textColor = "#FF6666";
config1.waveTextColor = "#FF9999";
config1.waveColor = "rgba(255, 51, 51,0.5)";
config1.circleThickness = 0.2;
config1.textVertPosition = 0.2;
config1.waveAnimateTime = 1000;

var prev;

$.get( "/sensor/4", function(data) {
        if(parseInt(data)<=0){
            $('#temp').html('Temperature ( - )');
            var res = -data;
            prev = res;
            var gauge2 = loadLiquidFillGauge("fillgauge2", res, config2);
        }else{
            $('#temp').html('Temperature ( + )');
            prev = data;
            var gauge2 = loadLiquidFillGauge("fillgauge2", data, config1);
        }
        
});

$(function() {
    setInterval(updating, 2000);
});

function updating(){
    $.get( "/sensor/4", function(data) {
        if(parseInt(data)<=0){
            $('#temp').html('Temperature ( - )');
            var res = -data;
            if(!prev==res){
                gauge2.update(res);
            }
        }else{
            $('#temp').html('Temperature ( + )');
            if(!prev==data){
                gauge2.update(data);
            }
        }
        
    });
}

$(document).ready(function(){
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
	// graphic logistics
	$('#bar').change(function(){
		if ($(this).prop('checked')) {
			$('#smoothie-accelerometer').hide();
			$('#bars').hide();
			$('#bar-accelerometer').show();
		}
	});
	$('#smoothie').change(function(){
		if ($(this).prop('checked')) {
			$('#bar-accelerometer').hide();
			$('#smoothie-accelerometer').show();
			$('#bars').show();
		}
	});

	$('#acc').on('click',function(){
		$.removeCookie('minVal');
		$.removeCookie('maxVal');
		$.removeCookie('minValBar');
		$.removeCookie('maxValBar');
		$.removeCookie('sensor');
		$.removeCookie('text');
		$.removeCookie('uM');

		$.cookie('minVal',-1.10);
		$.cookie('maxVal',1.10);
		$.cookie('minValBar',-1);
		$.cookie('maxValBar',1);
		$.cookie('sensor',1);
		$.cookie('text','Accelerometer');
		$.cookie('uM','g');

		$('#sens-text').html($.cookie('text'));

		upGraph();

		$('#acc-modal').modal('show');
	});
	$('#gyr').on('click',function(){
		$.removeCookie('minVal');
		$.removeCookie('maxVal');
		$.removeCookie('minValBar');
		$.removeCookie('maxValBar');
		$.removeCookie('sensor');
		$.removeCookie('text');
		$.removeCookie('uM');

		$.cookie('minVal',-30);
		$.cookie('maxVal',30);
		$.cookie('minValBar',-30);
		$.cookie('maxValBar',30);
		$.cookie('sensor',2);
		$.cookie('text','Gyroscope');
		$.cookie('uM','rads');

		$('#sens-text').html($.cookie('text'));

		upGraph();

		$('#acc-modal').modal('show');
	});
	$('#mag').on('click',function(){
		$.removeCookie('minVal');
		$.removeCookie('maxVal');
		$.removeCookie('minValBar');
		$.removeCookie('maxValBar');
		$.removeCookie('sensor');
		$.removeCookie('text');
		$.removeCookie('uM');

		$.cookie('minVal',-500);
		$.cookie('maxVal',500);
		$.cookie('minValBar',-500);
		$.cookie('maxValBar',500);
		$.cookie('sensor',3);
		$.cookie('text','Magnetometer');
		$.cookie('uM','ut');

		$('#sens-text').html($.cookie('text'));

		upGraph();

		$('#acc-modal').modal('show');
	});

});