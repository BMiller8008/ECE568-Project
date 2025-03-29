from machine import UART
from micropyGPS import MicropyGPS
import time

# Initialize GPS Parser Module
gps = MicropyGPS()

# UART2 on GPIO7 (RX) and GPIO8 (TX)
uart = UART(2, baudrate=9600, tx=8, rx=7, timeout=10)

print("Reading GPS data...")

while True:
    if uart.any():
        line = uart.readline()
        if line:
            try:
                line = line.decode('utf-8').strip()
                for char in line:
                    sentence_type = gps.update(char)
                if sentence_type:
                    formatted_coordinates = (gps.latitude, gps.longitude)
                    speed = gps.speed_string('kph')
                    print(formatted_coordinates, speed)
            except:
                pass
    time.sleep(1)
