#coding: UTF-8
"""
Script: Trame/probe
Création: rdouet, le 25/05/2021
"""


# Imports
from abc import ABC, abstractmethod
from BddService import *

# Programme principal
class Probe(ABC):
    @abstractmethod
    def canParse(self, senderId):
        pass

    @abstractmethod
    def parse(self, sqliteService, data):
        pass

class Co2Probe(Probe):

    def canParse(self, senderId):
        return senderId == b'\xFF\xD5\xA8\x0A'

    def parse(self, sqliteService, frame):
        co2 = frame[8] * 10
        hum = frame[7] / 2
        temp = frame[9] * 51 / 255
        sqliteService.updateCo2(co2, hum, temp)
        sqliteService.ventilationOnOff()


class CovProbe(Probe):
    def canParse(self, senderId):
        return senderId == b'\xFF\xD5\xA8\x0F'

    def parse(self, sqliteService, frame):
        cov = frame[7] + frame[8]
        sqliteService.updateCov(cov)
        sqliteService.ventilationOnOff()


class PmProbe(Probe):
    def canParse(self, senderId):
        return senderId == b'\xFF\xD5\xA8\x14'

    def parse(self, sqliteService, frame):
        pm1 = frame[7] * 2 + frame[8] // 128
        pm2 = (frame[8] * 4 + frame[9] // 64) & 511 # On applique un masque pour ne garder que les 9 octets de poids faible
        pm10 = (frame[9] * 8 + frame[10] // 32) & 511 # On applique un masque pour ne garder que les 9 octets de poids faible
        sqliteService.updatePm(pm1, pm2, pm10)
        sqliteService.ventilationOnOff()