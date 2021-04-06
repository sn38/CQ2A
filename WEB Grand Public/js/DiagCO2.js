$(function () {
    var x = document.getElementById("graphCO2").getAttribute("1")
    x = parseInt(x)
    $('#graphCO2').highcharts({
         title: {
        text: 'Evolution du taux de CO2 (dernière 24H)'
    },

    yAxis: {
        title: {
            text: 'taux de CO2 (ppm)'
        }
    },

    xAxis: {
        accessibility: {
            rangeDescription: 'Range: 0H to 24H'
        }
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 0
        }
    },

    series: [{
        name: 'CO2',
        data: [800, 1200, 1500, 2000, 900, 800, 1350, 1100, 800, 1200, 1500, 2000, 900, 700, 500, 900, 1200, 1300, 1450, 670, 900, 1500, 1670, 2000, 2100, 1240, 1670, 2000, 2100, 1240]
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});
});