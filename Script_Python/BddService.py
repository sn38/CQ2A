# coding: UTF-8
"""
Script: Trame/BddService
Création: rdouet, le 25/05/2021
"""

# Import
import sqlite3
import requests
from time import sleep
import serial
from datetime import datetime

# Programme principal
class BddService:
    connection_sqlite = None
    _filePath = "/var/www/html/adminer/bdd_sondes.db"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
# ------------------------------------ CONNECTION TO THE SQLITE DATABASE -------------------------------------- #
    def connectToBdd(self):
        self.connection_sqlite = sqlite3.connect(self._filePath)

# --------------------------------------- UPDATING THE SQLITE DATABASE -----------------------------------------#
    def updateCo2(self, val_co2, val_hum, val_temp):
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            self.connectToBdd()
            cursor = self.connection_sqlite.cursor()
            update_val = 'UPDATE donnees_sondes SET co2 = ?, humidite = ?, temperature = ? WHERE id = 1'
            data = (val_co2, val_hum, val_temp)
            cursor.execute(update_val, data)
            self.connection_sqlite.commit()
            cursor.close()
            self.connection_sqlite.close()

            print("===========================================================================")
            print("["+current_time+"] Co2:", val_co2, "\n["+current_time+"] Humidité:", val_hum, "\n["+current_time+"] Température:", val_temp)
            print("["+current_time+"] Co2, humidity and temperature updated in the SQLite database !")
            print("===========================================================================")
        except:
            print("/!\ Accès de la base de données SQLite pour le Co2 est temporairement impossible !")

    def updateCov(self, val_cov):
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            self.connectToBdd()
            cursor = self.connection_sqlite.cursor()
            update_val = 'UPDATE donnees_sondes SET cov = ? WHERE id = 1'
            data = (val_cov,)
            cursor.execute(update_val, data)
            self.connection_sqlite.commit()
            cursor.close()
            self.connection_sqlite.close()

            print("===========================================================================")
            print("["+current_time+"] COV:", val_cov)
            print("["+current_time+"] COV updated in the SQLite database !")
            print("===========================================================================")

        except:
            print("/!\ Accès de la base de données SQLite pour le COV est temporairement impossible !")

    def updatePm(self, val_pm1, val_pm2, val_pm10):
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            self.connectToBdd()
            cursor = self.connection_sqlite.cursor()
            update_val = 'UPDATE donnees_sondes SET pm1 = ?, pm2 = ?, pm10 = ? WHERE id = 1'
            data = (val_pm1, val_pm2, val_pm10)
            cursor.execute(update_val, data)
            self.connection_sqlite.commit()
            cursor.close()
            self.connection_sqlite.close()

            print("===========================================================================")
            print("["+current_time+"] PM1:", val_pm1, "\n["+current_time+"] PM2.5:", val_pm2, "\n["+current_time+"] PM10:", val_pm10)
            print("["+current_time+"] PM updated in the SQLite database !")
            print("===========================================================================")

        except:
            print("/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\ ")
            print("["+self.current_time+"] /!\ Accès de la base de données SQLite pour les PM est temporairement impossible ! /!\ ")
            print("/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\ ")

    # --------------------- GETTING THE DATA FROM THE SQLITE DATABASE ---------------------- #
    def postUpdateMysql(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        self.connectToBdd()
        cursor_sqlite = self.connection_sqlite.cursor()
        select_val = 'SELECT * FROM donnees_sondes WHERE id = 1'
        cursor_sqlite.execute(select_val)
        donnees = cursor_sqlite.fetchone()
        cursor_sqlite.close()
        self.connection_sqlite.close()

        # --------------------------- UPDATING THE DATABASE MYSQL ------------------------------ #
        formdata = {'co2': donnees[1], 'cov': donnees[2], 'hum': donnees[3], 'temp': donnees[4],
                    'pm1': donnees[5], 'pm2': donnees[6], 'pm10': donnees[7]}
        requests.post('https://cq2a.lycee-lgm.fr/scriptpython/envoi_mysql.php', data=formdata)
        print("===========================================================================")
        print("["+current_time+"] Mise a jour de la base de donnees MySQL reussi !")
        print("===========================================================================")


    def ventilationOnOff(self):
        self.connectToBdd()
        cursor = self.connection_sqlite.cursor()
        select_val = 'SELECT * FROM donnees_sondes WHERE id = 1'
        cursor.execute(select_val)
        donnees_sql = cursor.fetchone()
        cursor.close()
        self.connection_sqlite.close()

        if donnees_sql[1] > 1400 or donnees_sql[2] >= 450 or donnees_sql[5] >= 25 or donnees_sql[6] >= 25  or donnees_sql[7] >= 50:

            serialPort = serial.Serial('/dev/ttyAMA0', 57600, timeout=0.1)  # ou 'com14' PC Windows
            sleep(0.1)
            serialPort.write(
                b'\x55\x00\x07\x07\x01\x7a\xf6\x50\xff\xfb\xd8\x80\x30\x02\xff\xff\xff\xff\x7f\x00\x5c')  # id EnoceanPI
            sleep(0.1)
            serialPort.close()


        elif donnees_sql[1] < 1200 or donnees_sql[2] < 300 or donnees_sql[5] < 20 or donnees_sql[6] < 20 or donnees_sql[7] < 40:

            serialPort = serial.Serial('/dev/ttyAMA0', 57600, timeout=0.1)  # ou 'com14' PC Windows
            sleep(0.1)
            serialPort.write(
                b'\x55\x00\x07\x07\x01\x7a\xf6\x70\xff\xfb\xd8\x80\x30\x02\xff\xff\xff\xff\x7f\x00\xa2')  # id EnoceanPI
            sleep(0.1)
            serialPort.close()

# Fin

