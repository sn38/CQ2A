<!--index.php -->
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" integrity="sha384-B0vP5xmATw1+K9KRQjQERJvTumQW0nPEzvF6L/Z6nronJ3oUOFUFpCjEUQouq2+l" crossorigin="anonymous">
        <link rel="stylesheet" href="style.css" />
        <title> Historique CQ2A </title>
    </head>

    <body>

        <div class="conteneur">
            <?php include("includes/menu.php"); ?>

                <form action="" method="POST">
                    <p> Historique des données en fonction de la date : 
                        <input type="date" name="datej" />
                        <input type="submit" name="submit" />
                    </p>
                </form>
            
            <article>
                <?php
            try {
               
                if (isset($_POST['datej'])){
                     $ma_date = $_POST['datej'];

            
                // On se connecte à MySQL
                $destinataire='mysql:host=localhost;dbname=bdd_qualiteair;port='; $utilisateur='root'; $mdp=''; 
                $bdd = new PDO($destinataire, $utilisateur, $mdp);
                $reponse =  $bdd->prepare("SELECT * FROM qualiteairdonnees WHERE date_jour=:ma_date");
                $reponse->execute(array('ma_date' => $ma_date)); 
                ?>
            
            <table class="table">

                <thead class="thead-dark">
                    <tr>  
                        <th scope="col"> <?php echo ('Heure');?> </th>
                        <th scope="col"> <?php echo ('CO2'); ?> </th>
                        <th scope="col"> <?php echo ('COV'); ?> </th>
                        <th scope="col"> <?php echo ('PM 1'); ?> </th>
                        <th scope="col"> <?php echo ('PM 2.5'); ?> </th>
                        <th scope="col"> <?php echo ('PM 10'); ?> </th>
                        <th scope="col"> <?php echo ('Humidité'); ?> </th>
                        <th scope="col"> <?php echo ('Température'); ?> </th>
                    </tr> 
                </thead>
                <tbody>
                <?php 
                while ($ligne = $reponse->fetch(PDO::FETCH_ASSOC))
                {  
                ?>
                
                <tr>
                    <td scope="row"> <?php echo $ligne['heure_jour'];?></td>
                    <td> <?php echo $ligne['tauxco2'].' ppm';?></td>
                    <td> <?php echo $ligne['tauxcov'].' ppm'; ?></td>
                    <td> <?php echo $ligne['tauxpm1'].' μg/m³';?></td>
                    <td> <?php echo $ligne['tauxpm2'].' μg/m³';?></td>
                    <td> <?php echo $ligne['tauxpm10'].' μg/m³';?></td>
                    <td> <?php echo $ligne['humidite'].'%'.' HR';?></td>
                    <td> <?php echo $ligne['temperature'].'°C';?></td>
                </tr>  

                <?php
                    }
                ?>
            </tbody>
            </table>

            <?php
                $reponse = $bdd->prepare('SELECT AVG(tauxco2) as tauxco2_moy,
                                                AVG(tauxcov) as tauxcov_moy,
                                                AVG(tauxpm1) as tauxpm1_moy,
                                                AVG(tauxpm2) as tauxpm2_moy,
                                                AVG(tauxpm10) as tauxpm10_moy,
                                                AVG(temperature) as temperature_moy,
                                                AVG(humidite) as humidite_moy, heure_jour
                                        FROM qualiteairdonnees
                                        WHERE date_jour=:ma_date');
                $reponse->execute(array('ma_date' => $ma_date));
            ?>
                <table class="table">

                <thead class="thead-dark">
                    <tr>  
                        <th scope="col"> <?php echo ('Date');?> </th>
                        <th scope="col"> <?php echo ('Moyenne CO2'); ?> </th>
                        <th scope="col"> <?php echo ('Moyenne COV'); ?> </th>
                        <th scope="col"> <?php echo ('Moyenne PM 1'); ?> </th>
                        <th scope="col"> <?php echo ('Moyenne PM 2.5'); ?> </th>
                        <th scope="col"> <?php echo ('Moyenne PM 10'); ?> </th>
                        <th scope="col"> <?php echo ('Moyenne Humidité'); ?> </th>
                        <th scope="col"> <?php echo ('Moyenne Température'); ?> </th>
                    </tr> 
                </thead>
                <tbody>
                <?php 
                while ($ligne = $reponse->fetch(PDO::FETCH_ASSOC))
                {  
                ?>
                
                <tr>
                    <td scope="row"> <?php echo $ma_date ;?></td>
                    <td> <?php echo round($ligne['tauxco2_moy'], 2).' ppm';?></td>
                    <td> <?php echo round($ligne['tauxcov_moy'], 2).' ppm'; ?></td>
                    <td> <?php echo round($ligne['tauxpm1_moy'], 2).' μg/m³';?></td>
                    <td> <?php echo round($ligne['tauxpm2_moy'], 2).' μg/m³';?></td>
                    <td> <?php echo round($ligne['tauxpm10_moy'], 2).' μg/m³';?></td>
                    <td> <?php echo round($ligne['humidite_moy'], 2).'%'.' HR';?></td>
                    <td> <?php echo round($ligne['temperature_moy'], 2).'°C';?></td>
                </tr>  

                <?php
                    }
                ?>
            </tbody>
            </table> 
            <?php
                $reponse->closeCursor(); // Termine le traitement de la requête
                }}
            catch(Exception $e)
            {
                // En cas d'erreur précédemment, on affiche un message et on arrête tout
                die('Erreur : '.$e->getMessage());
            }

             ?>

                  

            </article>

        </div>

        <?php include("includes/pieddepage.php"); ?>

    </body>

</html>