from machine import UART, Pin
from micropyGPS import MicropyGPS
import time

# # Intialize GPS EN pin as GPIO26 on ESP32
gps_en = Pin(26, Pin.OUT)
gps_en.value(1)

# Initialize GPS Parser Module
gps = MicropyGPS()

# UART2 on GPIO7 (RX) and GPIO8 (TX)
uart = UART(2, baudrate=9600, tx=8, rx=7, timeout=10)

def read_gps_data():
    if gps_en.value():
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
    else:
        print("GPS is disabled (EN pin LOW)")

def main():
    print("Starting GPS Logger...")
    while True:
        read_gps_data()
        time.sleep(1)

main()
