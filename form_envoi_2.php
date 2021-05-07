<!--
<?php
if(isset($_POST["submit"])){
		$defilement = $_POST["defilement"];
		$position = $_POST["position"];
		$police = $_POST["police"];


		$destinataire = 'mysql:host=localhost;dbname=parametre;port=3306';
		$utilisateur = 'root';
		$motdepasse = '';
		$connexion = new PDO($destinataire,$utilisateur,$motdepasse);
		$connexion_sqlite = $sqlite3.connect('C:\Users\adrid\Desktop\Site web projet\SiteWebTechnicien.sqlite');
  		$cursor = $connexion_sqlite.cursor();
        $update_val = 'UPDATE parametre SET PositionDuTexte = $position, Defilement = $defilement, Police = $position, WHERE id = 1';

        $reponse=$connexion->prepare($update_val);
        $reponse->execute(array($update_val));
        print("Mise a jour de la base de donnees SQLite reussi !");
        $reponse->close(); }
?>
-->