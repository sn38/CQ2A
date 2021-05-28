# coding: UTF-8
"""
Script: Trame/BddService
Création: rdouet, le 25/05/2021
"""

# Import
import sqlite3
import requests

# Programme principal
class BddService:
    connection_sqlite = None
    _filePath = "P:/Documents/PROJET/DB/bdd_sondes.db"

# ------------------------------------ CONNECTION TO THE SQLITE DATABASE -------------------------------------- #
    def connectToBdd(self):
        self.connection_sqlite = sqlite3.connect(self._filePath)

# --------------------------------------- UPDATING THE SQLITE DATABASE -----------------------------------------#
    def updateCo2(self, val_co2, val_hum, val_temp):
        self.connectToBdd()
        cursor = self.connection_sqlite.cursor()
        update_val = 'UPDATE donnees_sondes SET co2 = ?, humidite = ?, temperature = ? WHERE id = 1'
        data = (val_co2, val_hum, val_temp)
        cursor.execute(update_val, data)
        self.connection_sqlite.commit()
        cursor.close()
        self.connection_sqlite.close()
        print("===========================================================================")
        print("Co2, humidity and temperature updated in the SQLite bdd !")
        print("===========================================================================")

    def updateCov(self, val_cov):
        self.connectToBdd()
        cursor = self.connection_sqlite.cursor()
        update_val = 'UPDATE donnees_sondes SET cov = ? WHERE id = 1'
        data = (val_cov,)
        cursor.execute(update_val, data)
        self.connection_sqlite.commit()
        cursor.close()
        self.connection_sqlite.close()
        print("===========================================================================")
        print("Cov updated in bdd !")
        print("===========================================================================")

    def updatePm(self, val_pm1, val_pm2, val_pm10):
        self.connectToBdd()
        cursor = self.connection_sqlite.cursor()
        update_val = 'UPDATE donnees_sondes SET pm1 = ?, pm2 = ?, pm10 = ? WHERE id = 1'
        data = (val_pm1, val_pm2, val_pm10)
        cursor.execute(update_val, data)
        self.connection_sqlite.commit()
        cursor.close()
        self.connection_sqlite.close()
        print("====================================================")
        print("PM updated in bdd !")
        print("====================================================")
    # --------------------- GETTING THE DATA FROM THE SQLITE DATABASE ---------------------- #
    def postUpdateMysql(self):
        self.connectToBdd()
        cursor = self.connection_sqlite.cursor()
        select_val = 'SELECT * FROM donnees_sondes WHERE id = 1'
        cursor.execute(select_val)
        donnees = cursor.fetchone()
        cursor.close()
        self.connection_sqlite.close()

        # --------------------------- UPDATING THE DATABASE MYSQL ------------------------------ #
        formdata = {'co2': donnees[1], 'cov': donnees[2], 'hum': donnees[3], 'temp': donnees[4],
                    'pm1': donnees[5], 'pm2': donnees[6], 'pm10': donnees[7]}
        requests.post('https://cq2a.lycee-lgm.fr/scriptpython/envoi_mysql.php', data=formdata)
        print("===========================================================================")
        print("Mise a jour de la base de donnees MySQL reussi !")
        print("===========================================================================")
# Fin
