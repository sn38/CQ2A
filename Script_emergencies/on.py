# Imports
import serial
import time

# Programme principal
def main():
    serialPort = serial.Serial('/dev/ttyAMA0', 57600, timeout=0.1)  # ou 'com14' PC Windows
    time.sleep(0.1)
    serialPort.write(b'\x55\x00\x07\x07\x01\x7a\xf6\x50\xff\xfb\xd8\x80\x30\x02\xff\xff\xff\xff\x7f\x00\x5c') #id EnoceanPI
    time.sleep(0.1)
    serialPort.close()
if __name__ == '__main__':
    main()