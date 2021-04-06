<!--index.php -->
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" integrity="sha384-B0vP5xmATw1+K9KRQjQERJvTumQW0nPEzvF6L/Z6nronJ3oUOFUFpCjEUQouq2+l" crossorigin="anonymous">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script type="text/javascript" src="http://code.highcharts.com/highcharts.js"></script>
        <link rel="stylesheet" href="style.css" />
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/modules/series-label.js"></script>
        <script src="https://code.highcharts.com/modules/exporting.js"></script>
        <script src="https://code.highcharts.com/modules/export-data.js"></script>
        <script src="https://code.highcharts.com/modules/accessibility.js"></script>
        <script>
             $(document).ready(function() {
                 //$("#actualise").load("actualise.php");
               var refreshId = setInterval(function() {
                  $("#actualise").load('actualise.php?randval='+ Math.random());
               }, 60000);
               $.ajaxSetup({ cache: false });
            });
        </script>
        

        <title> Accueil CQ2A </title>
    </head>

    <body>

        <div class="conteneur">
            
            <?php include("includes/menu.php"); ?>

            <h1>QUALITÉ DE L'AIR DANS UN AMPHITHÉÂTRE</h1>

                <div id="horloge"> 

                    <script type="text/javascript"> // affiche l'heure en temps réel
                        function horloge(){
                        var div = document.getElementById("horloge");
                        var heure = new Date();
                        div.firstChild.nodeValue = heure.getHours()+":"+heure.getMinutes()+":"+heure.getSeconds();
                        window.setTimeout("horloge()",1000);
                        }
                        horloge();
                    </script>
                    <?php
                     setlocale(LC_TIME, 'fra_fra');// affiche la date actuelle
                    echo '<d class="date">Jour : '.strftime('%A %d %B %Y</d>');
                ?> 
                </div>

                <div id="actualise">
                    <?php include('actualise.php'); ?>
                </div>

            <script type="text/javascript" src="js/DiagCO2.js"></script>
            <div class="graph">
                <div class="text-center" id="graphCO2" 1="8" style="width: 65%; height: 300px"></div>
            </div>
            <script type="text/javascript" src="js/DiagCOV.js"></script>
            <div class="graph">
                <div id="graphCOV" 1="8" style="width: 65%; height: 300px"></div>
            </div>
            <script type="text/javascript" src="js/DiagParticules.js"></script>
             <div class="graph">
                <div class="text-center" id="graphParticules" 1="8" style="width: 65%; height: 300px"></div>
            </div>
            <script type="text/javascript" src="js/DiagHumidite.js"></script>
             <div class="graph">
                <div class="text-center" id="graphHumidite" 1="8" style="width: 65%; height: 300px"></div>
            </div>
            <script type="text/javascript" src="js/DiagTemperature.js"></script>
             <div class="graph">
                <div class="text-center" id="graphTemperature" 1="8" style="width: 65%; height: 300px"></div>
            </div>
        </div>
      

        <?php include("includes/pieddepage.php"); ?>

    </body>

</html>