
<?php
    $destinataire='mysql:host=localhost;dbname=bdd_qualiteair;port='; $utilisateur='root'; $mdp=''; 
    $bdd = new PDO($destinataire, $utilisateur, $mdp);

    $reponse = $bdd->query('SELECT tauxco2,tauxcov,tauxpm1,tauxpm2,tauxpm10,temperature,humidite
                            FROM qualiteairdonnees
                            WHERE id=(SELECT MAX(id) AS idMax FROM qualiteairdonnees)');
    $donnees = $reponse->fetch();
                    
        if( ($donnees['tauxco2']>=1200 && $donnees['tauxco2']<1400) 
            || ($donnees['tauxcov']>=300 && $donnees['tauxcov']<450)
            || ($donnees['tauxpm2']>=15 && $donnees['tauxpm2']<25)
            || ($donnees['tauxpm10']>=20 && $donnees['tauxpm10']<30)
            || (($donnees['temperature']>=12 && $donnees['temperature']<16) || ($donnees['temperature']>=24 && $donnees['temperature']<28))
            || (($donnees['humidite']>=25 && $donnees['humidite']<30) || ($donnees['humidite']>=70 && $donnees['humidite']<75))
            ){
                echo '<p class="Indicateur">Qualité air actuelle: <d class="MoyenneIndicateur">Moyenne</d></p>';
            }
        elseif( ($donnees['tauxco2']>=1400 && $donnees['tauxco2']<2500) 
            || ($donnees['tauxcov']>=450 && $donnees['tauxcov']<600)
            || ($donnees['tauxpm2']>=25 && $donnees['tauxpm2']<100)
            || ($donnees['tauxpm10']>=30 && $donnees['tauxpm10']<100)
            || (($donnees['temperature']>=0 && $donnees['temperature']<12) || ($donnees['temperature']>=28 && $donnees['temperature']<50))
            || (($donnees['humidite']>=0 && $donnees['humidite']<25) || ($donnees['humidite']>=75 && $donnees['humidite']<100))
            ){
                echo '<p class="Indicateur">Qualité air actuelle : <d class="MauvaiseIndicateur">Mauvaise</d></p>';
            }
        else{
                echo '<p class="Indicateur">Qualité air actuelle : <d class="BonneIndicateur">Bonne</d></p>';
            }
?>

<div class='DonneesAffichage'>
    <h2>Données actuelles :</h2>
    </br>
       Taux de CO2 :
            <?php echo ($donnees['tauxco2'].' ppm');?>
    </br>
        Taux de COV :
            <?php echo ($donnees['tauxcov'].' ppm');?>
    </br>
        Taux de particules PM1 :
            <?php echo ($donnees['tauxpm1'].' μg/m³');?>
    </br>
        Taux de particules PM2.5 :
            <?php echo ($donnees['tauxpm2'].' μg/m³');?>
    </br>
        Taux de particules PM10 :
            <?php echo ($donnees['tauxpm10'].' μg/m³');?>
    </br>
        Température :
            <?php echo ($donnees['temperature'].'°C');?>
    </br>
        Taux d'humidité :
            <?php echo ($donnees['humidite'].'%'.' HR'.' (humidité relative)');?>
</div>