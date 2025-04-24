import time
from machine import UART, Pin
import socket
import network
from micropyGPS import MicropyGPS
from accelerometer import get_acceleration
import _thread  # for multicore support on ESP32
import esp32

# Global shared variable (must be protected if writing from both threads)
current_speed = 0
speed_lock = _thread.allocate_lock()

# Constants
threshold = 1.7  # m/s
dt = 0.1  # interval in seconds

# Setup pin
en_pin = Pin(26, Pin.OUT)

# WiFi details
SSID = "Will"
PASSWORD = "thedawgsRout"
ADDR = ("172.20.10.11", 8000)
RECV_BUFFER_SIZE = 1024

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Connected to WiFi:", wlan.ifconfig()[0])

def send_to_host(coords, time_data):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
        msg = f"UPDATE {coords[0]} {coords[1]} {time_data[0]} {time_data[1]}\n"
        s.send(msg.encode())
        #s.recv(RECV_BUFFER_SIZE)
        s.close()
        print("Data sent to host.")
    except Exception as e:
        print("Send failed:", e)

def gps_wifi_thread():
    gps = MicropyGPS()
    uart = UART(2, baudrate=9600, tx=8, rx=7, timeout=10)

    connect_wifi()

    while True:
        speed_lock.acquire()
        local_speed = current_speed
        speed_lock.release()

        if local_speed > threshold:
            en_pin.on()
            print("GPS Enabled")

            if uart.any():
                try:
                    line = uart.readline()
                    if line:
                        line = line.decode('utf-8').strip()
                        for char in line:
                            sentence_type = gps.update(char)
                        if sentence_type:
                            coords = (gps.latitude, gps.longitude)
                            send_to_host(coords, (0, 0))
                            print("GPS:", coords)
                except:
                    print("GPS parsing failed.")
        else:
            en_pin.off()

        time.sleep(1)  # reduce GPS polling frequency to save power

def accel_thread():
    global current_speed

    Vx = Vy = 0.0

    while True:
        ax, ay, az, _ = get_acceleration()

        ax = ax if abs(ax) > 1 else 0
        ay = ay if abs(ay) > 1 else 0

        Vx += ax * dt
        Vx *= 0.9
        Vx = Vx if abs(Vx) > 0.1 else 0

        Vy += ay * dt
        Vy *= 0.9
        Vy = Vy if abs(Vy) > 0.1 else 0

        speed = (Vx**2 + Vy**2)**0.5

        speed_lock.acquire()
        current_speed = speed
        speed_lock.release()

        print("Speed:", speed)

        time.sleep(dt)

# Main entry
def main():
    _thread.start_new_thread(gps_wifi_thread, ())  # Run on Core 0
    accel_thread()  # Run on Core 1 (main)

if __name__ == "__main__":
    main()
