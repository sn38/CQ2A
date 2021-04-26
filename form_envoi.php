<?php
if(isset($_POST["submit"])){
		connexion_sqlite = sqlite3.connect('C:\Users\adrid\Desktop\Site web projet\SiteWebTechnicien')
  		cursor = self.connexion_sqlite.cursor()
        update_val = 'UPDATE parametre SET PositionDuTexte = ?, Defilement = ?, Police = ?, WHERE id = 1'
        data = (Position_Police, Position_du_texte, type_police)
        cursor.execute(update_val, data)
        self.connexion_sqlite.commit()
        print("Mise a jour de la base de donnees SQLite reussi !")
        cursor.close() 
?>