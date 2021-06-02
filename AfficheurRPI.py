# coding: UTF-8
"""
Script: pythonProject9/Afficheur
Création: abouillet, le 19/03/2021
"""


# Imports
import serial
from time import sleep
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


# --------------------Fonction defilement------------------- #
tuple=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

list_defilement = {
    0 : b'61',
    1 : b'62',
    2 : b'63',
    3 : b'65',
    4 : b'66',
    5 : b'67',
    6 : b'68',
    7 : b'69',
    8 : b'6A',
    9 : b'6B',
    10 : b'6C',
    11 : b'6D',
    12 : b'6F',
    13 : b'70',
    14 : b'71',
    15 : b'72',
    16 : b'73',
    17 : b'74',
}

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

# ------------------- Acquisition de la base de données raspberry pour les sondes ------------------#
def get_bdd_sqlite(parametre, id_bdd):
    #print("donne = ", parametre, "id =", id_bdd)
    connexion_sqlite = sqlite3.connect('/var/www/html/adminer/bdd_sondes.db')
    #connexion_sqlite = sqlite3.connect('bdd_sondes.db')
    cursor = connexion_sqlite.cursor()
    get_valeur = "SELECT " + str(parametre) + " FROM donnees_sondes WHERE id = ?"
    data = (id_bdd,)
    cursor.execute(get_valeur, data)

    bdd_donne = cursor.fetchone()
    cursor.close()
    connexion_sqlite.close()
    #print(bdd_donne[0])
    return bdd_donne[0]

# ------------------- Acquisition de la base de données raspberry pour le site web ------------------#
"""def get_bdd_sqlite2(parametre_afficheur, id_bdd):
    #print("donnees =", parametre_afficheur, "id =" , id_bdd)
    connexion_sqlite = sqlite3.connect('SiteWebTechnicien.db')
    cursor = connexion_sqlite.cursor()
    get_valeur = "SELECT " + str(parametre_afficheur) + " FROM donnees_afficheur WHERE id = ?"
    data = (id_bdd,)
    cursor.execute(get_valeur, data)

    bdd_donne = cursor.fetchone()
    cursor.close()
    connexion_sqlite.close()

    return bdd_donne"""

# ----------- Ajouts des couleurs et des parametre selon la valeurs ------------------------------

def affichage(etat_co2, taux_co2, etat_cov,taux_cov, etat_hum, taux_hum, etat_pm2, taux_pm2, etat_pm10, taux_pm10, etat_temp, taux_temp, taux_pm1):
    color_co2 = color(etat_co2)  # Appel de la fonction color
    color_cov = color(etat_cov)
    color_hum = color(etat_hum)
    color_pm2 = color(etat_pm2)
    color_pm10 = color(etat_pm10)
    color_temp = color(etat_temp)

    #taux_co2 = int(taux_co2).to_bytes(3, 'big')


# ----------------------- Connexion au Port COM5 ----------------------------------

    #ser = serial.Serial(port='COM5', baudrate=9600, timeout=0, rtscts=1)  # ouverture du port serial
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # ouverture du port serial

# ----------------------------- Trame de l'afficheur ------------------------------

    #ser.write(b" _01Z00_02AA_1B_30_61_1E_31_"+color_co2+b" CO2 "+b"%d"%(taux_co2)+b" PPM _0D_"+color_cov+b" COV "+b"%d"%(taux_cov)+b" PPB _0D_"+color_hum+b" Humidite "+b"%d"%(taux_hum)+b" % _0D_1C1 "+b"%d"%(taux_pm1)+b" PM1 _0D_"+color_pm2+b""+b"%d"%(taux_pm2)+b" PM2 _0D_"+color_pm10+b""+b"%d"%(taux_pm10)+b" PM1O _0D_"+color_temp+b""+b"%d"%(taux_temp)+b" Degres _10A_04")
    ser.write(b" _01Z00_02AA_1B_30_61_1E_31_"+color_temp+b" Temperature : "+b"%d"%(taux_temp)+b" Degres _0D_"+color_hum+b" Humidite "+b"%d"%(taux_hum)+b" % _0D_"+color_co2+b" CO2 "+b"%d"%(taux_co2)+b" PPM _0D_"+color_cov+b" COV "+b"%d"%(taux_cov)+b" PPB _0D_1C1 "+b"%d"%(taux_pm1)+b" PM1 _0D_"+color_pm2+b""+b"%d"%(taux_pm2)+b" PM2 _0D_"+color_pm10+b""+b"%d"%(taux_pm10)+b" PM1O _10A_04")

    ser.close()

# --------------------Fonction couleur-------------------#
def color(etat):
    if etat == "bon":
        return b'1C2'  #vert
    elif etat == "moyen":
        return  b'1C8'  #jaune
    else :
        return b'1C1'  #rouge


#----------------------- Programme principal -----------------
def main():
    while True:
    # -----------------------Parametre afficheur-------------------------

    # ------------------------- Défilement -------------------------------

        #valeur_defilement = 1
        #valeur_defilement = get_bdd_sqlite2("Defilement", 1)  # valeur pour la fonction defilement BDD
        #print ("Defilement = ",valeur_defilement) # verification reception
        #valeur_bin_defilement = b"61"  # valeur pour l'affichage en binaire
    # ------------------------- Position -------------------------------
        #valeur_position = 1
        #valeur_position = get_bdd_sqlite2("PositionDuTexte", 1)  # valeur pour la fonction position BDD
        #print ("PositionDuTexte = ",valeur_position) # verification reception
        #valeur_bin_position = b"30"  # valeur pour l'affichage en binaire
        #position(valeur_position)
    # ------------------------- Police -------------------------------
        #valeur_police = 1
        #valeur_police = get_bdd_sqlite2("Police", 1)  # valeur pour la fonction police BDD
        #print ("Police = ",valeur_police) # verification reception
        #valeur_bin_police = b"31"  # valeur pour l'affichage en binaire
        #police(valeur_police)
    # -------------------Valeur des sondes----------------

    # ------------------------  COV ----------------------
        #valeur_cov = 200
        taux_cov = get_bdd_sqlite("cov", 1)  # valeur pour la fonction cov BDD
        print("cov = ",taux_cov) # verification reception
        #valeur_bin_cov = b"+taux_cov+"    # valeur pour l'affichage en binaire
        etat_cov = cov(taux_cov)    # attribution des notations textuels moyen bon tres bon

    #------------------------  CO2 ------------------------------------
        #valeur_co2 = 1300
        taux_co2 = get_bdd_sqlite("co2", 1) # valeur pour la fonction co2 BDD
        print("co2 =",taux_co2) # verification reception
        #valeur_bin_co2 = b"1300"
        etat_co2 = co2(taux_co2)

    # -------------------------- HUMIDITE ------------------------------
        #valeur_hum = 35
        taux_hum = get_bdd_sqlite("humidite", 1)  # valeur pour la fonction hum BDD
        print("humidite =",taux_hum) # verification reception
        #valeur_bin_hum = b'35'
        etat_hum = hum(taux_hum)

    #--------------------------- Particule PM 1 -----------------------

        taux_pm1 = get_bdd_sqlite("pm1" , 1)
        print("pm1 =", taux_pm1)

    #-------------------------- Particule PM 2.5 ----------------------

        #valeur_pm2 = 35
        taux_pm2 = get_bdd_sqlite("pm2", 1)  # valeur pour la fonction pm2 BDD
        print("pm2 =",taux_pm2) # verification reception
        #valeur_bin_pm2 = b'35'
        etat_pm2 = pm2(taux_pm2)

    #--------------------------- Particule 10 -------------------------
        #valeur_pm10 = 35
        taux_pm10 = get_bdd_sqlite("pm10", 1)  # valeur pour la fonction pm10 BDD
        print("pm10 =",taux_pm10) # verification reception
        #valeur_bin_pm10 = b'35'
        etat_pm10 = pm10(taux_pm10)

    #--------------------------- Température ---------------------------

        #valeur_temp = 20
        taux_temp = get_bdd_sqlite("temperature", 1)  # valeur pour la fonction temp BDD
        print ("temp  =",taux_temp) # verification reception
        #valeur_bin_temp = b'20'
        etat_temp = temp(taux_temp)

    #-------------------------- Affichage ------------------------------

        affichage(etat_co2, taux_co2, etat_cov,taux_cov, etat_hum, taux_hum, etat_pm2, taux_pm2, etat_pm10, taux_pm10, etat_temp, taux_temp, taux_pm1)

    #------------ Vérification si le port est utililsé ----------------

        #print(ser.name)  # check which port was really used
        print("================================================")
        sleep(20)



if __name__ == '__main__':
    main()
# Fin
