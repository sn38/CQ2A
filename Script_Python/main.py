# coding: UTF-8
"""
Script: Trame/main.py
Création: rdouet, le 25/05/2021
"""


# Imports
from time import sleep
import threading

from BddService import BddService
from FrameInterceptor import FrameInterceptor
from Probe.ProbeDispatcher import ProbeDispatcher, NoProbeFoundException


# Fonctions
def getData(interceptor, dispatcher, sqliteService):
    while True:
        try:
            frame = interceptor.intercept()
            probe = dispatcher.getProbe(frame)
            probe.parse(sqliteService, frame)

        except NoProbeFoundException:
            pass

def postMysql(sqliteService):
    while True:
        sqliteService.postUpdateMysql()
        sleep(60)


# Programme principal
def main():
    interceptor = FrameInterceptor()
    dispatcher = ProbeDispatcher()
    sqliteService = BddService()

    threading.Thread(target=getData, args=(interceptor, dispatcher, sqliteService)).start()
    threading.Thread(target=postMysql, args=(sqliteService,)).start()

if __name__ == '__main__':
    main()
# Fin
