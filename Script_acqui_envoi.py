# coding: UTF-8
"""
Script: Orienté_Objets_Personnages/main
Création: rdouet, le 19/03/2021
"""


# Imports
import sqlite3
import time
import serial
import mysql.connector

# Class
class acquisition_frame:
    def __init__(self):
        self.co2 = None
        self.cov = None
        self.hum = None
        self.temp = None
        self.pm1 = None
        self.pm2 = None
        self.pm10 = None
        self.serialPort = None

    def connexion_port(self):
        self.serialPort = serial.Serial("/dev/ttyAMA0", 57600, timeout=0.1)  # serial.Serial(/dev/ttyAMA0 , baudrate, timeout=Y)

    def recuperation_data(self):
        while True:
            # We are waitting for 24 bytes or above frame 4BS
            if self.serialPort.inWaiting() >= 24:
                frame = self.serialPort.read(self.serialPort.inWaiting())
                print('\n\nTrame brut: ', frame)
                print('Trame en hexa: ', frame.hex())
                idSender = frame[11:11 + 4]
                print('Lecture de l\'ID Sender: ', idSender.hex())

                # We check if the id of the sensor are inside the frame received and we show data
                if idSender == b'\xff\xd5\xa8\x0a':
                    print('C02:', frame[8] * 10, 'ppm')
                    print('Humidite:', frame[7] / 2, '%')
                    print('Temperature:', frame[9] * 51 / 255, '°C')
                    self.co2 = frame[8] * 10
                    self.hum = frame[7] / 2
                    self.temp = frame[9] * 51 * 255

                if idSender == b'\xff\xd5\xa8\x0f':
                    print('COV:', frame[7] * 255 + frame[8],
                          "ppb")  # frame[7] don't really increase but the frame[8] increase his value
                    self.cov = frame[7] * 255 + frame[8]

                if idSender == b'\xFF\xD5\xA8\x14':
                    print('PM1:', frame[7] * 2 + frame[8] // 128, 'PM2.5:', frame[8] * 4 + frame[9] // 64, 'PM10:',
                          frame[9] * 8 + frame[10] // 32)
                    self.pm1 = frame[7] * 2 + frame[8] // 128
                    self.pm2 = frame[8] * 4 + frame[9] // 64
                    self.pm10 = frame[9] * 8 + frame[10] // 32

                time.sleep(1)


class bdd:
# --------------------------------------- CONSTRUCTOR ------------------------------------------------ #
    def __init__(self):
        self.connexion_sqlite = None
        self.connexion_mysql = None

# ------------------------------ CONNEXION TO THE DATABASE SQLITE ------------------------------------ #
    def connexion_bdd_sqlite(self):
        self.connexion_sqlite = sqlite3.connect('/var/www/html/adminer/bdd_sondes.db')

# ------------------------------ CONNEXION TO THE DATABASE MYSQL ------------------------------------- #
    def connexion_bdd_mysql(self):
        self.connexion_mysql = mysql.connector.connect(user="root", password="password",
                                                       host="172.16.126.21", database="bdd_qualiteair")

# -------------------------------- UPDATING THE DATABASE SQLITE -------------------------------------- #
    def set_bdd_sqlite(self, val_c02, val_cov, val_humi, val_temp, val_pm1, val_pm2, val_pm10):
        cursor = self.connexion_sqlite.cursor()
        update_val = 'UPDATE donnees_sondes SET co2 = ?, cov = ?, humidite = ?, temperature = ?, pm1 = ?, pm2 = ?, pm10 = ? WHERE id = 1'
        data = (val_c02, val_cov, val_humi, val_temp, val_pm1, val_pm2, val_pm10)
        cursor.execute(update_val, data)
        self.connexion_sqlite.commit()
        print("Mise a jour de la base de donnees SQLite reussi !")
        cursor.close()
        
# ----------------------- CREATING A NEW ENTRY IN THE DATABASE MYSQL -------------------------------- #
    def set_bdd_mysql(self, val_c02, val_cov, val_pm1, val_pm2, val_pm10, val_temp, val_hum):
        cursor = self.connexion_mysql.cursor()
        insert_val = "INSERT INTO qualiteairdonnees (tauxco2, tauxcov, tauxpm1, tauxpm2, tauxpm10, temperature, humidite) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (val_c02, val_cov, val_pm1, val_pm2, val_pm10, val_temp, val_hum)
        cursor.execute(insert_val, data)
        self.connexion_mysql.commit()
        print("Mise a jour de la base de donnees MySQL reussi !")

        cursor.close()
        
# Programme principal
def main():
    x = 0

# -------------------------------- CREATING THE OBJECT USING THE CLASS "bdd" -------------------------------------- #
    bdd_sqlite = bdd()
    bdd_mysql = bdd()
# ------------------------------------------ CONNECTION TO DATABASES ---------------------------------------------- #
    bdd_sqlite.connexion_bdd_sqlite()
    bdd_mysql.connexion_bdd_mysql()

    while True:
        x = x +1
        bdd_sqlite.set_bdd_sqlite(1100, 350, 80, 16, 30, 20, x) #co2 - cov - humidite - temperature - pm1 - pm2 - pm10
        bdd_mysql.set_bdd_mysql(1000, 200, 1, 2, 10, 20, 52) #co2 - cov - pm1 - pm2 - pm10 - temperature - humidite
        print("\n==================================================================\n")
        time.sleep(60)

if __name__ == '__main__':
    main()
# Fin
