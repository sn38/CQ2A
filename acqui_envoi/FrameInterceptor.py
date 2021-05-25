# coding: UTF-8
"""
Script: Trame/FrameInterceptor
Création: rdouet, le 25/05/2021
"""
# Import
import serial

# Programme principal
class FrameInterceptor:
    _serialPort = "/dev/ttyAMA0"
    _speed = 57600
    _time_out = 0.1

    def intercept(self):
        serialPort = serial.Serial("com7", 57600, timeout=0.1)  # serial.Serial(/dev/ttyAMA0 , baudrate, timeout=Y)
        while True:
            # We are waitting for 24 bytes or above, frame 4BS
            if serialPort.inWaiting() >= 24:
                frame = serialPort.read(serialPort.inWaiting())
                return frame

            return None

# Fin
