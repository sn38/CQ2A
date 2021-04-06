 <?php
 
                    $reponse = $bdd->query("SELECT tauxCO2,tauxCOV,tauxParticules,temperature,humidite FROM qualiteairdonnees WHERE (DATE_FORMAT(last_update, '%d %M %Y') = $_Get['date']");
                    $reponse->execute();

                    while ($donnees = $reponse->fetch())
                    {
                ?>  
                        <option> <?php echo ($donnees['tauxCO2'].$donnees['tauxCOV'].$donnees['tauxParticules'].$donnees['temperature'].$donnees['humidite']));?></option>
                <?php
                    }
                ?>