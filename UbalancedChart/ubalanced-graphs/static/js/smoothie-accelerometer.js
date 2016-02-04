$(document).ready(function(){
	function myYRangeFunction() {
			// TODO implement your calculation using range.min and range.max
			var min = $.cookie('minVal');
			var max = $.cookie('maxVal');
			return {min: min, max: max};
	}

	var chart = new SmoothieChart({millisPerPixel:1,grid:{strokeStyle:'#fdfcff'},labels:{fontSize:12,precision:4},yRangeFunction:myYRangeFunction}),
	canvas = document.getElementById('smoothie-accelerometer'),
	Xseries = new TimeSeries();
	Yseries = new TimeSeries();
	Zseries = new TimeSeries();
	
	// Add a random value to each line every second
	setInterval(function() {
		var maxi = $.cookie('maxVal');
		$.get( "/sensor/" + $.cookie('sensor'), function(data) {
			res = data.split(',');
			Xseries.append(new Date().getTime(),res[0]);
			Yseries.append(new Date().getTime(),res[1]);
			Zseries.append(new Date().getTime(),res[2]);
			
			if(res[0]<0){
				str1 = (res[0]*100)/maxi + '%';
				$('#xlabl').html('-x:&nbsp;');
			}else{
				str1 = (res[0]*100)/maxi + '%';
				$('#xlabl').html('+x:&nbsp;');
			}
			if(res[1]<0){
				str2 = (res[1]*100)/maxi + '%';
				$('#ylabl').html('-y:&nbsp;');
			}else{
				str2 = (res[1]*100)/maxi + '%';
				$('#ylabl').html('+y:&nbsp;');
			}
			if(res[2]<0){
				str3 = (res[2]*100)/maxi + '%';
				$('#zlabl').html('-z:&nbsp;');
			}else{
				str3 = (res[2]*100)/maxi + '%';
				$('#zlabl').html('+z:&nbsp;');
			}

			$('#x-prog').width(str1);
			$('#y-prog').width(str2);
			$('#z-prog').width(str3);
    	});
	}, 500);

	chart.addTimeSeries(Xseries,{lineWidth:4,strokeStyle:'#00ff00'});
	chart.addTimeSeries(Yseries,{lineWidth:4,strokeStyle:'#6699ff'});
	chart.addTimeSeries(Zseries,{lineWidth:4,strokeStyle:'#ff432e'});
	chart.streamTo(canvas, 1309);
});
	

