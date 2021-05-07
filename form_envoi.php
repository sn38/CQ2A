<?php
$defilement = $_POST["defilement"];
$position = $_POST["position"];
$police = $_POST["police"];

// Connexion
$bdd = new SQLite3('SiteWebTechnicien.db');
// Inserer ici les requêtes
$q = $bdd->exec('UPDATE Parametre SET PositionDuTexte = $position, Defilement = $defilement, Police = $position, WHERE id = 1');
// Deconnexion
$bd = null;
?>







