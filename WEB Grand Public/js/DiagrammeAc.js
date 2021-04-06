$(function () {
    var x = document.getElementById("graphique").getAttribute("1")
    x = parseInt(x)
    $('#graphique').highcharts({
        chart: {
            type: 'bar' // pie pour des graphiques en camembert
        },
        title: {
            text: x
        },
        xAxis: {
            categories: ['Pommes', 'Bananes', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Nombre de fruits mangés'
            }
        },
        // Les données de notre graphique
        series: [{
            name: 'Jane',
            data: [x, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
    });
});