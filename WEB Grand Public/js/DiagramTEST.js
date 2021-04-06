Highcharts.setOptions({
 global: { useUTC: false }
});
Highcharts.chart('container_temp', {
    chart: {
        type: 'spline',
        scrollablePlotArea: {
            minWidth: 600,
            scrollPositionX: 1
        }
    },
    title: {
        text: 'Temperature sur 24 heures'
    },
    xAxis: {
        type: 'datetime',
        labels: {
            overflow: 'justify'
        },        
    },
    yAxis: {
        title: {
            text: 'Temperature °C'
        },
        minorGridLineWidth: 0,
        gridLineWidth: 0,
        alternateGridColor: null, 
    },
    tooltip: {
        valueSuffix: ' °C'
    },
    plotOptions: {
        spline: {
            lineWidth: 4,
            states: {
                hover: {
                    lineWidth: 5
                }
            },
            marker: {
                enabled: false
            },
            pointInterval: 300000,
          pointStart:<?php echo strtotime($data_label[0])*1000;?>
             
        }
    },
    series: [{
        name: 'Temp',
        data: [<?php echo join($data, ',') ?>],
        color: '#00c0ef'
         
 
        },
    ],
    navigation: {
        menuItemStyle: {
            fontSize: '10px'
        }
    }
});