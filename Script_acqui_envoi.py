# coding: UTF-8
"""
Script: Script_acqui_envoi.py
Création: Robin DOUET
Date: 19/03/2021
"""

# Imports
import sqlite3
from time import sleep
import serial
import requests
import threading
import statistics

# Class
class frame_manager:
    # ---------------------------------------- CONSTRUCTOR ------------------------------------------------ #
    def __init__(self, co2, cov, hum, temp, pm1, pm2, pm10):
        self.co2 = co2
        self.cov = cov
        self.hum = hum
        self.temp = temp
        self.pm1 = pm1
        self.pm2 = pm2
        self.pm10 = pm10
    # -------------------------- GETTING EVERY INFORMATIONS INSIDE THE FRAME ------------------------------ #
    def get_data(self, co2, cov, hum, temp, pm1, pm2, pm10):
        serialPort = serial.Serial("/dev/ttyAMA0", 57600, timeout=0.1) #serial.Serial(/dev/ttyAMA0 , baudrate, timeout=Y)
        while True:
                # We are waitting for 24 bytes or above, frame 4BS
                if serialPort.inWaiting() >= 24:
                    frame = serialPort.read(serialPort.inWaiting())
                    print('\nTrame brut: ', frame)
                    print('Trame en hexa: ', frame.hex())
                    idSender = frame[11:11 + 4]  # recuperation of the id sender
                    print('\nLecture de l\'ID Sender: ', idSender)

                # We check if the id of the sensor are inside the frame received and we show data
                    # ------------------- GETTING THE CO2, HUMIDITY & TEMPERATURE ------------------- #
                    if idSender == b'\xff\xd5\xa8\x0a':
                        print('C02:', frame[8] * 10, 'ppm')
                        print('Humidite:', frame[7] / 2, '%')
                        print('Temperature:', frame[9] * 51 / 255, '°C')
                        co2.append(frame[8] * 10)
                        hum.append(frame[7] / 2)
                        temp.append(frame[9] * 51 / 255)
                        bdd.set_bdd_sqlite_co2(frame[8]*10, frame[7]/2, frame[9]*51/255)

                    # ------------------------------ GETTING THE COV -------------------------------- #
                    elif idSender == b'\xff\xd5\xa8\x0f':
                        print('COV:', frame[7] * 255 + frame[8],"ppb")
                        cov.append(frame[7] * 255 + frame[8])
                        bdd.set_bdd_sqlite_cov(frame[7] * 255 + frame[8])

                    # ----------------------- GETTING THE PM1, PM2.5, PM10 -------------------------- #
                    elif idSender == b'\xFF\xD5\xA8\x14':
                        print('PM1:', frame[7] * 2 + frame[8] // 128, "µ/m^3")
                        print('PM2.5:', frame[8] * 4 + frame[9] // 64, "µ/m^3")
                        print('PM10:', frame[9] * 8 + frame[10] // 32, "µ/m^3")
                        pm1.append(frame[7] * 2 + frame[8] // 128)
                        pm2.append(frame[8] * 4 + frame[9] // 64)
                        pm10.append(frame[9] * 8 + frame[10] // 32)
                        bdd.set_bdd_sqlite_pm(frame[7]*2+frame[8]//128, frame[8]*4+frame[9]//64, frame[9]*8+frame[10]//32)
                sleep(2)
                return


class bdd:
    # ---------------------------------------- CONSTRUCTOR ------------------------------------------------ #
    def __init__(self):
        self.connexion_sqlite = None

    # ------------------------------ CONNECTION TO THE DATABASE SQLITE ------------------------------------ #
    def connection_bdd_sqlite(self):
        self.connexion_sqlite = sqlite3.connect('/var/www/html/adminer/bdd_sondes.db')

    # -------------------------------- UPDATING THE DATABASE SQLITE --------------------------------------- #
    def set_bdd_sqlite_co2(self, val_c02, val_humi, val_temp):
        cursor = self.connexion_sqlite.cursor()
        update_val = 'UPDATE donnees_sondes SET co2 = ?, humidite = ?, temperature = ? WHERE id = 1'
        data = (val_c02, val_humi, val_temp)
        cursor.execute(update_val, data)
        self.connexion_sqlite.commit()
        print("Mise a jour du co2, de l'humidité et de la température de la base de données SQLite reussi !")
        cursor.close()

    def set_bdd_sqlite_cov(self, val_cov):
        cursor = self.connexion_sqlite.cursor()
        update_val = 'UPDATE donnees_sondes SET cov = ? WHERE id = 1'
        data = val_cov
        cursor.execute(update_val, data)
        self.connexion_sqlite.commit()
        print("Mise a jour du cov de la base de données SQLite reussi !")
        cursor.close()

    def set_bdd_sqlite_pm(self, val_pm1, val_pm2, val_pm10):
        cursor = self.connexion_sqlite.cursor()
        update_val = 'UPDATE donnees_sondes SET pm1 = ?, pm2 = ?, pm10 = ? WHERE id = 1'
        data = (val_pm1, val_pm2, val_pm10)
        cursor.execute(update_val, data)
        self.connexion_sqlite.commit()
        print("Mise a jour du pm1, du pm2.5 et du pm10 de la base de données SQLite reussi !")
        cursor.close()

    # ------------------ CALL A PHP SCRIPT FOR SENDING THE DATA IN THE MYSQL DATABASE --------------------- #
    def set_bdd_mysql(self, co2, cov, pm1, pm2, pm10, temp, hum):
        while True:
            formdata = {'co2':statistics.mean(co2), 'cov':statistics.mean(cov), 'pm1':statistics.mean(pm1),
                        'pm2':statistics.mean(pm2), 'pm10':statistics.mean(pm10),
                        'temp':statistics.mean(temp), 'hum':statistics.mean(hum)}

            requests.post('https://cq2a.lycee-lgm.fr/scriptpython/envoi_mysql.php', data=formdata)
            print("Mise a jour de la base de donnees MySQL reussi !")
            sleep(20)


# Programme principal
def main():
    # -------------- CREATING THE OBJECT USING THE CLASS "bdd" & "frame_manager" AND THE LIST ------------- #
    co2 = [1] # Exploiter les exceptions de la méthode "mean" pour réinitialiser les lists
    hum = [1]
    temp = [1]
    cov = [1]
    pm1 = [1]
    pm2 = [1]
    pm10 = [1]
    senders = frame_manager(co2, cov, hum, temp, pm1, pm2, pm10)
    bdd_sqlite = bdd()
    bdd_mysql = bdd()

    # --------------------------------- CONNECTION TO DATABASES & PORTS------------------------------------ #
    bdd_sqlite.connection_bdd_sqlite()

    # ----------------------------- SENDING THE DATA LIST TO THE DATABASES ---------------------------------#
    threading.Thread(target=senders.get_data, args=(co2, cov, pm1, pm2, pm10, temp, hum)).start()
    threading.Thread(target=bdd_mysql.set_bdd_mysql, args=(co2, cov, pm1, pm2, pm10, temp, hum)).start()
if __name__ == '__main__':
    main()
# Fin
