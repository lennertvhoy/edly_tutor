Highcharts.theme = {
	accessibility: {
		enabled: false
	},
	colors: ['#4572A7', '#78B25A', '#FF9900','#89A54E', '#80699B', '#3D96AE', '#DB843D', '#92A8CD', '#A47D7C', '#3366CC','#DC3912','#FF9900'],
	chart: {
		backgroundColor: 'transparent',
	},
	title: {
		align: 'left',
		style: {
			fontFamily:'"Open Sans","Trebuchet MS",arial,verdana,sans-serif', 
			fontSize:'16px'
		}
	},
	xAxis: {
		type:'datetime',
		tickWidth: 0,
		gridLineWidth: 0,
		labels: {
			style: {
				fontFamily:'"Open Sans","Trebuchet MS",arial,verdana,sans-serif', 
				fontSize:'14px'
			},
			maxStaggerLines: 1,
			overflow: 'justify',
			step:3,
			formatter: function () {
				//if date is in d/m/Y h:s format put time in the next line
				if(this.value.match(/\d+\/\d+\/\d+ \d+:\d+/)){
					dt=this.value.split(' ');
					label=dt[0]+'<br>'+dt[1];
				}
				else if(this.value.match(/\w+, \w+ \d+/)){
					dt=this.value.split(',');
					label=dt[0]+'<br>'+dt[1];
				}
				else{
					label=this.value;
				}
				return label;
			}
		}
	},
	yAxis: {
		title: { text: ''},
		min: 0,
		labels: {
        	style: {
        		fontFamily:'"Open Sans","Trebuchet MS",arial,verdana,sans-serif',
        		fontSize:'14px'
        	}
		}
	},
	legend: {
		symbolRadius: 0,
		itemStyle: {
			fontWeight: 'normal',
			fontSize:'14px'
		}
	},
	credits: false,
	plotOptions: {
		area: {
			marker: {
				enabled: false
			},
			animation: {
				duration: 500
			}
		},
		areaspline: {
            fillOpacity: 0.5,
            marker: {
				enabled: false
			},
			animation: {
				duration: 500
			}
        },
		pie: {
			animation: {
				duration: 500
			},
			allowPointSelect: true,
			cursor: 'pointer',
			depth: 35,
			dataLabels: {
				enabled: true
			},
			showInLegend: true,
			tooltip: {
	            pointFormat: '<strong>{point.y} ({point.percentage:.1f}%)</strong>'
			},
			borderColor: null,
			//Notstarted inprogress complete
			colors: ['#AA2C25','#FF773C','#78B25A'],
			
			//passed notpassed pending
			altcolors:['#46A546','#9D261D','#F89406']
		},
	}
};

$(document).ready(function(){
	setTimeout( function(){$(window).trigger('redraw-graph-on-load');}, 200);
	$('.tl-set-report-interval').on('click',function(){$(window).trigger('resize');});
	
	var waitForFinalEvent = (function(){
		var timers = {};
		return function(callback, ms, uniqueId){

			if(!uniqueId){
				uniqueId = "uniqueId";
			}
    
			if(timers[uniqueId]){
				clearTimeout(timers[uniqueId]);
			}
			timers[uniqueId] = setTimeout(callback, ms);
		};
	})();
	
	$(window).on('resize redraw-graph-on-load', function(){
		waitForFinalEvent(function(){
			
			if($('.tl-graph-area').length && Highcharts.charts.length){
				
				if($(window).width()<979){
				
					if($(window).width()<768){
						$(".tl-graph-area").highcharts().xAxis[0].update({labels: {rotation:-45, style: {fontSize:'12px'} }});
					}
					else{
						$(".tl-graph-area").highcharts().xAxis[0].update({labels: {rotation:0, style: {fontSize:'12px'} }});
					}
				}
				else{
					
					if($('.tl-content-half').length){
						$(".tl-graph-area").highcharts().xAxis[0].update({labels: {rotation:0, style: {fontSize:'12px'}}});
					}
					else{
						$(".tl-graph-area").highcharts().xAxis[0].update({labels: {rotation:0, style: {fontSize:'14px'}}});
					}
					
				}
			}
		}, 500, "...");
	});
});

var highchartsOptions = Highcharts.setOptions(Highcharts.theme);