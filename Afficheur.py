# coding: UTF-8
"""
Script: pythonProject9/Afficheur
Création: abouillet, le 19/03/2021
"""


# Imports
import serial
import time
import sqlite3

# Fonctions

#-----------------------taux avec couleur------------------#
def cov(taux_cov):

    if taux_cov < 300:
        etat_cov = "bon"

    else:
        if 300 < taux_cov <= 450:
            etat_cov = "moyen"

        else:
            if taux_cov > 450:
                etat_cov = "mauvais"

    return etat_cov


def co2(taux_co2):

    if taux_co2 < 1200:
        etat_co2 = "bon"

    else:
        if 1200 < taux_co2 <= 1400:
            etat_co2 = "moyen"

        else:
            if taux_co2 > 1400:
                etat_co2 = "mauvais"

    return etat_co2

def hum(taux_hum):

    if 30 < taux_hum < 70:
        etat_hum = "bon"

    else:
        if 25 <= taux_hum <= 30 or 70 <= taux_hum <= 75:
            etat_hum = "moyen"

        else:
            if taux_hum < 25 or taux_hum > 75 :
                etat_hum = "mauvais"

    return etat_hum

def temp(taux_temp):

    if 18 < taux_temp < 22:
        etat_temp = "bon"

    else:
        if 15 <= taux_temp <= 18 or 12 <= taux_temp <= 27:
            etat_temp = "moyen"

        else:
            if taux_temp < 15 or taux_temp > 27 :
                etat_temp = "mauvais"

    return etat_temp

def pm2(taux_pm2):

        if taux_pm2 <= 25:
            etat_pm2 = "bon"

        else:
            if taux_pm2 > 25:
                etat_pm2 = "mauvais"

        return etat_pm2

def pm10(taux_pm10):

        if taux_pm10 <= 50:
            etat_pm10 = "bon"

        else:
            if taux_pm10 > 50:
                etat_pm10 = "mauvais"

        return etat_pm10


# --------------------Fonction defilement-------------------#

def defilement(valeur_defilement):
    if valeur_defilement == 1:
        valeur_bin_defilement = b'61'
    if valeur_defilement == 2:
        valeur_bin_defilement = b'62'
    if valeur_defilement == 3:
        valeur_bin_defilement = b'63'
    if valeur_defilement == 4:
        valeur_bin_defilement = b'65'
    if valeur_defilement == 5:
        valeur_bin_defilement = b'66'
    if valeur_defilement == 6:
        valeur_bin_defilement = b'67'
    if valeur_defilement == 7:
        valeur_bin_defilement = b'68'
    if valeur_defilement == 8:
        valeur_bin_defilement = b'69'
    if valeur_defilement == 9:
        valeur_bin_defilement = b'6A'
    if valeur_defilement == 10:
        valeur_bin_defilement = b'6B'
    if valeur_defilement == 11:
        valeur_bin_defilement = b'6C'
    if valeur_defilement == 12:
        valeur_bin_defilement = b'6D'
    if valeur_defilement == 13:
        valeur_bin_defilement = b'6F'
    if valeur_defilement == 14:
        valeur_bin_defilement = b'70'
    if valeur_defilement == 15:
        valeur_bin_defilement = b'71'
    if valeur_defilement == 16:
        valeur_bin_defilement = b'72'
    if valeur_defilement == 17:
        valeur_bin_defilement = b'73'
    if valeur_defilement == 18:
        valeur_bin_defilement = b'74'

    return valeur_bin_defilement

# --------------------Fonction Position-------------------#

def position(valeur_position):
    if valeur_position == "gauche":
        valeur_bin_position = b'31'
    if valeur_position == "centre":
        valeur_bin_position = b'30'
    return valeur_bin_position

# --------------------Fonction Police-------------------#

def police(valeur_police):
    if valeur_police == "grande":
        valeur_bin_position = b'31'
    if valeur_police == "petite":
        valeur_bin_position = b'30'
    return valeur_bin_position

#---------------------- ajout dans la base de données-------------------------#

"""def set_bdd_sqlite(val_co2, val_cov,):   # FONCTIONNE
    connexion_sqlite = sqlite3.connect('Test_air.db')
    cursor = connexion_sqlite.cursor()
    update_val = 'UPDATE bdd_air SET co2 = ?, cov = ? WHERE id = 1'
    data = (val_co2, val_cov)
    cursor.execute(update_val, data)
    connexion_sqlite.commit()
    print("Mise a jour de la base de donnees SQLite reussi !")
    cursor.close()
    connexion_sqlite.close()"""

#------------------- Acquisition de la base de données raspberry pour les sondes ------------------#
def get_bdd_sqlite(donne, id_bdd):
    connexion_sqlite = sqlite3.connect('/var/www/html/adminer/bdd_sondes.db')
    cursor = connexion_sqlite.cursor()
    get_valeur = "SELECT ? FROM donnees_sondes WHERE id = ?"
    data = (donne, id_bdd)
    cursor.execute(get_valeur, data)

    bdd_donne = cursor.fetchone()
    cursor.close()
    connexion_sqlite.close()

    return bdd_donne
#------------------- Acquisition de la base de données raspberry pour le site web ------------------#

def get_bdd_sqlite2(donne, id_bdd):
    connexion_sqlite = sqlite3.connect('/var/www/html/adminer/SiteWebTechnicien.db')
    cursor = connexion_sqlite.cursor()
    get_valeur = "SELECT ? FROM parametre WHERE id = 1"
    data = (donne, id_bdd)
    cursor.execute(get_valeur, data)

    bdd_donne = cursor.fetchone()
    cursor.close()
    connexion_sqlite.close()

    return bdd_donne

#----------- Ajouts des couleurs et des parametre selon la valeurs ------------------------------

def affichage(valeur_bin_defilement,valeur_bin_position,valeur_bin_police, taux_co2, valeur_bin_co2, taux_cov, valeur_bin_cov, taux_hum, valeur_bin_hum, taux_pm2, valeur_bin_pm2, taux_pm10, valeur_bin_pm10, taux_temp, valeur_bin_temp):
    color_co2 = color(taux_co2)  # Appel de la fonction color
    color_cov = color(taux_cov)
    color_hum = color(taux_hum)
    color_pm2 = color(taux_pm2)
    color_pm10 = color(taux_pm10)
    color_temp = color(taux_temp)

#----------------------- Connexion au Port COM5 ----------------------------------

    ser = serial.Serial(port='COM5', baudrate=9600, timeout=0, rtscts=1)  # ouverture du port serial

#----------------------------- Trame de l'afficheur ------------------------------

    #ser.write(b"_01Z00_02AA_1B_30_61_1E_31_"+color_co2+b"CO2 "+valeur_bin_co2+b" ppm _0D_"+color_cov+b"COV "+valeur_bin_cov+b" ppb _0D_"+color_hum+b" Humidite "+valeur_bin_hum+b"% _0D_"+color_pm2+b"PM2 "+valeur_bin_pm2+b"_0D_"+color_pm10+b"PM10 "+valeur_bin_pm10+b"_0D_"+color_temp+b"Temperature "+valeur_bin_temp+b" degres _10A_04")
    ser.write(b"_01Z00_02AA_1B_"+valeur_bin_position+b"_"+valeur_bin_defilement+b"_1E_"+valeur_bin_police+b"_1C3 test 1 _0D_1C2 test 2 _10A_04")
    ser.write(b"_01Z00_02AA_1B_30_61_1E_31_1C1 test 1 _0D_1C2 test 2 _10A_04")
    ser.close()

#--------------------Fonction couleur-------------------#
def color(etat):
    if etat == "bon":
        color_frame = b'1C2'  #vert
    if etat == "moyen":
        color_frame = b'1C8'  #jaune
    if etat == "mauvais":
        color_frame = b'1C1'  #rouge

    return color_frame


#----------------------- Programme principal -----------------
def main():
    #set_bdd_sqlite(1300, 200) #ajout des valeurs dans la Bdd
    #get_bdd_sqlite() #acquisition des valeurs dans la bdd

# ------------------------- Défilement -------------------------------

    valeur_defilement = 1
    #defilement = get_bdd_sqlite("Defilement", 1)  # valeur pour la fonction defilement BDD
    # print ("Defilement ",valeur_temp) # verification reception
    valeur_bin_defilement = b"61"  # valeur pour l'affichage en binaire

# ------------------------- Position -------------------------------
    valeur_position = 1
    # defilement = get_bdd_sqlite("Defilement", 1)  # valeur pour la fonction defilement BDD
    # print ("Defilement ",valeur_temp) # verification reception
    valeur_bin_position = b"30"  # valeur pour l'affichage en binaire
# ------------------------- Police -------------------------------
    valeur_police = 1
    # defilement = get_bdd_sqlite("Defilement", 1)  # valeur pour la fonction defilement BDD
    # print ("Defilement ",valeur_temp) # verification reception
    valeur_bin_police = b"31"  # valeur pour l'affichage en binaire
# ------------------------  COV ----------------------
    valeur_cov = 200
    #valeur_cov = get_bdd_sqlite("cov", 1)  # valeur pour la fonction co2 BDD
    #print("cov ",valeur_cov) # verification reception
    valeur_bin_cov = b"200"    # valeur pour l'affichage en binaire
    etat_cov = cov(valeur_cov)    # attribution des notations textuels moyen bon tres bon

#------------------------  CO2 ------------------------------------
    valeur_co2 = 1300
    #valeur_co2 = get_bdd_sqlite("co2", 1)  # valeur pour la fonction co2 BDD
    #print("co2 ",valeur_co2) # verification reception
    valeur_bin_co2 = b"1300"
    etat_co2 = co2(valeur_co2)

# -------------------------- HUMIDITE ------------------------------
    valeur_hum = 35
    #valeur_hum = get_bdd_sqlite("hum", 1)  # valeur pour la fonction hum BDD
    #print("hum ",valeur_hum) # verification reception
    valeur_bin_hum = b'35'
    etat_hum = hum(valeur_hum)

#-------------------------- Particule PM 2.5 ----------------------

    valeur_pm2 = 35
    #valeur_pm2 = get_bdd_sqlite("pm2", 1)  # valeur pour la fonction pm2 BDD
    #print("pm2 ",valeur_pm2) # verification reception
    valeur_bin_pm2 = b'35'
    etat_pm2 = pm2(valeur_pm2)

#--------------------------- Particule 10 -------------------------
    valeur_pm10 = 35
    #valeur_pm10 = get_bdd_sqlite("pm10", 1)  # valeur pour la fonction pm10 BDD
    #print("pm10 ",valeur_pm10) # verification reception
    valeur_bin_pm10 = b'35'
    etat_pm10 = pm10(valeur_pm10)

#--------------------------- Température ---------------------------

    valeur_temp = 20
    #valeur_temp = get_bdd_sqlite("temp", 1)  # valeur pour la fonction temp BDD
    #print ("temp ",valeur_temp) # verification reception
    valeur_bin_temp = b'20'
    etat_temp = temp(valeur_temp)

#-------------------------- Affichage ------------------------------

    affichage(valeur_bin_defilement, valeur_bin_position, valeur_bin_police, etat_co2, valeur_bin_co2, etat_cov, valeur_bin_cov,etat_hum,valeur_bin_hum,etat_pm2,valeur_bin_pm2,etat_pm10,valeur_bin_pm10, etat_temp, valeur_bin_temp)

#------------ Vérification si le port est utililsé ----------------

    #print(ser.name)  # check which port was really used



if __name__ == '__main__':
    main()
# Fin
