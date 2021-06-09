# coding: UTF-8
"""
Script: Trame/FrameInterceptor
Création: rdouet, le 25/05/2021
"""
# Import
import serial
from time import sleep

# Programme principal
class FrameInterceptor:
    _serialPort = "/dev/ttyAMA0"
    _speed = 57600
    _time_out = 0.1

    def intercept(self):
        serialPort = serial.Serial(self._serialPort, self._speed, timeout=self._time_out)  # Connexion au port
        while True:
            sleep(0.1)
            # We are waitting for 24 bytes or above, frame 4BS
            if serialPort.inWaiting() >= 24:
                frame = serialPort.read(serialPort.inWaiting()) # On met la trame dans la variable "frame"
                return frame

            return None

# Fin
