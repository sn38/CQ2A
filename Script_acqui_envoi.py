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


# Class
class frame_manager:
    # ---------------------------------------- CONSTRUCTOR ------------------------------------------------ #
    def __init__(self):
        self.co2 = 'co2'
        self.cov = 'cov'
        self.hum = 'hum'
        self.temp = 'temp'
        self.pm1 = 'pm1'
        self.pm2 = 'pm2'
        self.pm10 = 'pm10'

    # -------------------------- GETTING EVERY INFORMATIONS INSIDE THE FRAME ------------------------------ #
    def get_data(self):
        serialPort = serial.Serial("/dev/ttyAMA0", 57600,
                                   timeout=0.1)  # serial.Serial(/dev/ttyAMA0 , baudrate, timeout=Y)

        # --------------------------------RESTART THE VALUES OF DATA ---------------------------------------#
        data = {self.co2:None, self.cov:None, self.hum:None, self.temp:None, self.pm1:None, self.pm2:None, self.pm10:None}
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
                        data[self.co2] = frame[8] * 10
                        data[self.hum] = frame[7] / 2
                        data[self.temp] = frame[9] * 51 / 255

                    # ------------------------------ GETTING THE COV -------------------------------- #
                    if idSender == b'\xff\xd5\xa8\x0f':
                        print('COV:', frame[7] * 255 + frame[8],
                              "ppb")  # frame[7] don't really increase but the frame[8] increase his value
                        data[self.cov] = frame[7] * 255 + frame[8]

                    # ----------------------- GETTING THE PM1, PM2.5, PM10 -------------------------- #
                    if idSender == b'\xFF\xD5\xA8\x14':
                        print('PM1:', frame[7] * 2 + frame[8] // 128, "µ/m^3")
                        print('PM2.5:', frame[8] * 4 + frame[9] // 64, "µ/m^3")
                        print('PM10:', frame[9] * 8 + frame[10] // 32, "µ/m^3")
                        data[self.pm1] = frame[7] * 2 + frame[8] // 128
                        data[self.pm2] = frame[8] * 4 + frame[9] // 64
                        data[self.pm10] = frame[9] * 8 + frame[10] // 32

                #print("\nValeurs incomplète => | Co2 :", self.co2, "ppm | Hum:", self.hum, "% | Temp:", self.temp, "°C | Cov:", self.cov, "ppb | PM1:", self.pm1,"µ/m^3 | PM2:", self.pm2, "µ/m^3 | PM10:", self.pm10, "µ/m^3 |")
                sleep(0.5)
                return data


class bdd:
    # ---------------------------------------- CONSTRUCTOR ------------------------------------------------ #
    def __init__(self):
        self.connexion_sqlite = None
        self.connexion_mysql = None

    # ------------------------------ CONNECTION TO THE DATABASE SQLITE ------------------------------------ #
    def connection_bdd_sqlite(self):
        self.connexion_sqlite = sqlite3.connect('/var/www/html/adminer/bdd_sondes.db')

    # -------------------------------- UPDATING THE DATABASE SQLITE --------------------------------------- #
    def set_bdd_sqlite(self, val_c02, val_cov, val_humi, val_temp, val_pm1, val_pm2, val_pm10):
        cursor = self.connexion_sqlite.cursor()
        update_val = 'UPDATE donnees_sondes SET co2 = ?, cov = ?, humidite = ?, temperature = ?, pm1 = ?, pm2 = ?, pm10 = ? WHERE id = 1'
        data = (val_c02, val_cov, val_humi, val_temp, val_pm1, val_pm2, val_pm10)
        cursor.execute(update_val, data)
        self.connexion_sqlite.commit()
        print("Mise a jour de la base de donnees SQLite reussi !")
        cursor.close()

    # ------------------ CALL A PHP SCRIPT FOR SENDING THE DATA IN THE MYSQL DATABASE --------------------- #
    def set_bdd_mysql(self, val_co2, val_cov, val_pm1, val_pm2, val_pm10, val_temp, val_hum):
        formdata = {'co2':val_co2, 'cov':val_cov, 'pm1':val_pm1, 'pm2':val_pm2, 'pm10':val_pm10, 'temp':val_temp, 'hum':val_hum}
        requests.post('https://cq2a.lycee-lgm.fr/scriptpython/envoi_mysql.php', data=formdata)
        print("Mise a jour de la base de donnees MySQL reussi !")

    def sending_bdd(self, data, bdd_sqlite, bdd_mysql):
        bdd_sqlite.set_bdd_sqlite(data[0], data[1], data[2], data[3], data[4], data[5], data[6])  # co2 - cov - humidite - temperature - pm1 - pm2 - pm10
        bdd_mysql.set_bdd_mysql(data[0], data[1], data[4], data[5], data[6], data[3], data[2])  # co2 - cov - pm1 - pm2 - pm10 - temperature - humidite
        sleep(60)

# Programme principal
def main():
    # -------------------- CREATING THE OBJECT USING THE CLASS "bdd" & "frame_manager"--------------------- #
    senders = frame_manager()
    bdd_sqlite = bdd()
    bdd_mysql = bdd()

    # --------------------------------- CONNECTION TO DATABASES & PORTS------------------------------------ #
    bdd_sqlite.connection_bdd_sqlite()

    # ------------------------------- SENDING THE DATA LIST TO THE DATABASES -------------------------------#
    data = threading.Thread(target=senders.get_data).start()
    senders_bdd = threading.Thread(target=bdd.sending_bdd, args=(data, bdd_sqlite, bdd_mysql))
    senders_bdd.start()

    print("\n==================================================================\n")


if __name__ == '__main__':
    main()
# Fin
