# #recieve the accelearation info from the accelerometer (x,y,z) 
# #calculate current speed ( Vnew = Vold + a * dt) for each direction (x,y,z)
# #calculate the magnitude of the speed (V = sqrt(Vx^2 + Vy^2 + Vz^2))
# #check if the abs speed is greater than 1.7 m/s, if so, send enable signal to GPS (our enabler is A0/GPIO 26 pin)
# #send enable signal to wifi server side, to make sure it only gets updated when EN is on 
# # make this an interrupt function, so that it can be called when the accelerometer is updated, have it call the accelerometer every 

# from machine import UART, Pin
# from micropyGPS import MicropyGPS
# from accelerometer import get_acceleration  
# from machine import Pin
# import time
# import socket
# import network
# from machine import Timer

# ADDR = ("172.20.10.2", 8000)

# senseTimer = Timer(0)
# DT = 500 # 0.1 seconds

# GPS_ON = 0
# V = 0
# Vx = 0
# Vy = 0
# Vz = 0
# FORMATTED_COORDINATES = []

# def sendToHost(GPS_coords, time):
#     global ADDR
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         client_socket.connect(ADDR)
#         print("Successfully connected to host.")
#         message = f"UPDATE {GPS_coords[0]} {GPS_coords[1]} {time[0]} {time[1]}\n"
#         client_socket.send(message.encode())
#         print("Sent message")
#         data = client_socket.recv(RECV_BUFFER_SIZE)
#         client_socket.close()
#         print("Connection closed.")
#     except:
#         print("Failed to connect to host")
        
# def connectWifi():
#     wlan = network.WLAN(network.WLAN.IF_STA)
#     wlan.active(True)
#     ssid = "iPhone1" # GRADER: change this
#     key = "c1fp7v272c0y2" # GRADER: change this
#     if not wlan.isconnected():
#         wlan.connect(ssid, key)
#         while not wlan.isconnected():
#             pass
#     ip = wlan.ifconfig()[0]
#     print(f"Connected to {ssid}\nIP Address: {ip}\n")
        
# def senseCallback(Timer):
#     global GPS_ON
#     global V
#     global Vx
#     global Vy
#     global Vz
#     Vx = 0.0
#     Vy = 0.0
#     Vz = 0.0
#     threshold = 0.2  # m/s
#     dt = 0.1  # time interval in seconds (50 ms)
    
#     en_pin = Pin(26, Pin.OUT)  # GPIO26 (A0) as GPS enable output


        
#     # Get acceleration values (in m/s²)
#     ax, ay, az, G = get_acceleration()
#     print("x:",ax)
#     print("y:",ay)
#     print ("G:", G)

#     # Speed integration
#     if True: 
#         ax = ax if abs(ax) > 1 else 0
#         ay = ay if abs(ay) > 1 else 0
       
        
#         Vx += ax * dt
#         Vx = Vx * 0.95
#         Vx = Vx if abs(Vx) > 0.1 else 0
        
#         Vy += ay * dt
#         Vy = Vy * 0.95
#         Vy = Vy if abs(Vy) > 0.1 else 0

#         # Magnitude of speed vector
#         V = (Vx**2 + Vy**2)**0.5
  
    
#         print("Current Speed:", V)

#         # Enable GPS if speed exceeds threshold
#         if V > threshold:
#             en_pin.on()
#             GPS_ON = 1
            
#             print("GPS Enabled")
#             # Initialize GPS Parser Module
            
                
                    
#         else:
#             GPS_ON = 0
#             en_pin.off()

#             print("GPS Disabled")


# def main():
#     global FORMATTTED_COORDINATES
#     FORMATTED_COORDINATES = []
#     connectWifi()
#     senseTimer.init(mode=Timer.PERIODIC, period=DT, callback=senseCallback)
    
#     while True:
#         if GPS_ON:
#             print("\n\n\n\n",GPS_ON)
#             gps = MicropyGPS()

#             # UART2 on GPIO7 (RX) and GPIO8 (TX)
#             uart = UART(2, baudrate=9600, tx=8, rx=7, timeout=10)
#             time.sleep(1)
#             if uart.any():
#                 line = uart.readline()
#                 if line:
#                     try:
#                         line = line.decode('utf-8').strip()
#                         for char in line:
#                             sentence_type = gps.update(char)
#                         if sentence_type:
#                             FORMATTED_COORDINATES = (gps.latitude, gps.longitude)
#                             speed = gps.speed_string('kph')
#                             #sendToHost(formatted_coordinates,(0,0))
#                             print(FORMATTED_COORDINATES, speed)
#                     except:
#                         print("FAIL")
#                         pass
#             print("Sending coordinates")
#             sendToHost(FORMATTED_COORDINATES, (0,0))
#         time.sleep(5)
    
#     '''
#     Vx = 0.0
#     Vy = 0.0
#     Vz = 0.0
#     threshold = 0.2  # m/s
#     dt = 0.1  # time interval in seconds (50 ms)
    
#     en_pin = Pin(26, Pin.OUT)  # GPIO26 (A0) as GPS enable output

    
#     while True:
        
#         # Get acceleration values (in m/s²)
#         ax, ay, az, G = get_acceleration()
#         print("x:",ax)
#         print("y:",ay)
#         print ("G:", G)

#         # Speed integration
        
#         ax = ax if abs(ax) > 1 else 0
#         ay = ay if abs(ay) > 1 else 0
       
        
#         Vx += ax * dt
#         Vx = Vx * 0.95
#         Vx = Vx if abs(Vx) > 0.1 else 0
        
#         Vy += ay * dt
#         Vy = Vy * 0.95
#         Vy = Vy if abs(Vy) > 0.1 else 0

#         # Magnitude of speed vector
#         V = (Vx**2 + Vy**2)**0.5
  
    
#         print("Current Speed:", V)

#         # Enable GPS if speed exceeds threshold
#         if V > threshold:
#             en_pin.on()
            
#             print("GPS Enabled")
#             # Initialize GPS Parser Module
#             gps = MicropyGPS()

#             # UART2 on GPIO7 (RX) and GPIO8 (TX)
#             uart = UART(2, baudrate=9600, tx=8, rx=7, timeout=10)
#             time.sleep(1)
#             if uart.any():
#                 line = uart.readline()
#                 if line:
#                     try:
#                         line = line.decode('utf-8').strip()
#                         for char in line:
#                             sentence_type = gps.update(char)
#                         if sentence_type:
#                             formatted_coordinates = (gps.latitude, gps.longitude)
#                             speed = gps.speed_string('kph')
#                             sendToHost(formatted_coordinates,(0,0))
#                             print(formatted_coordinates, speed)
#                     except:
#                         print("FAIL")
#                         pass
                
                    
#         else:
#             en_pin.off()

#             print("GPS Disabled")

#         time.sleep(dt)
#         '''

# # Start main function
# if __name__ == "__main__":
#     main()


recieve the accelearation info from the accelerometer (x,y,z) 
calculate current speed ( Vnew = Vold + a * dt) for each direction (x,y,z)
calculate the magnitude of the speed (V = sqrt(Vx^2 + Vy^2 + Vz^2))
check if the abs speed is greater than 1.7 m/s, if so, send enable signal to GPS (our enabler is A0/GPIO 26 pin)
send enable signal to wifi server side, to make sure it only gets updated when EN is on 
# make this an interrupt function, so that it can be called when the accelerometer is updated, have it call the accelerometer every 

from machine import UART, Pin
from micropyGPS import MicropyGPS
from accelerometer import get_acceleration  
from machine import Pin
import time



def sendToHost(GPS_coords, time):
    global ADDR
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
        print("Successfully connected to host.")
        message = f"UPDATE {GPS_coords[0]} {GPS_coords[1]} {time[0]} {time[1]}\n"
        client_socket.send(message.encode())
        print("Sent message")
        data = client_socket.recv(RECV_BUFFER_SIZE)
        client_socket.close()
        print("Connection closed.")
    except:
        print("Failed to connect to host")
        
def connectWifi():
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    ssid = "iPhone1" # GRADER: change this
    key = "c1fp7v272c0y2" # GRADER: change this
    if not wlan.isconnected():
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
    ip = wlan.ifconfig()[0]
    print(f"Connected to {ssid}\nIP Address: {ip}\n")
    
    
def main():
    
    #connectWIFI()
    
    Vx = 0.0
    Vy = 0.0
    Vz = 0.0
    threshold = 1.7  # m/s
    dt = 0.1  # time interval in seconds (50 ms)
    
    en_pin = Pin(26, Pin.OUT)  # GPIO26 (A0) as GPS enable output

    while True:
        
        # Get acceleration values (in m/s²)
        ax, ay, az, G = get_acceleration()
        print("x:",ax)
        print("y:",ay)
        print ("G:", G)

        # Speed integration
        
        ax = ax if abs(ax) > 1 else 0
        ay = ay if abs(ay) > 1 else 0
       
        
        Vx += ax * dt
        Vx = Vx * 0.95
        Vx = Vx if abs(Vx) > 0.1 else 0
        
        Vy += ay * dt
        Vy = Vy * 0.95
        Vy = Vy if abs(Vy) > 0.1 else 0

        # Magnitude of speed vector
        V = (Vx**2 + Vy**2)**0.5
  
    
        print("Current Speed:", V)

        # Enable GPS if speed exceeds threshold
        if V > threshold:
            
            en_pin.on()
            
            print("GPS Enabled")
            # Initialize GPS Parser Module
            gps = MicropyGPS()

            # UART2 on GPIO7 (RX) and GPIO8 (TX)
            uart = UART(2, baudrate=9600, tx=8, rx=7, timeout=10)
            time.sleep(1)
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
                           # sendToHost(formatted_coordinates, (0,0))
                            print(formatted_coordinates, speed)
                    except:
                        print("FAIL")
                        pass
                
                    
        else:
            en_pin.off()

            print("GPS Disabled")

        time.sleep(dt)

# Start main function
if __name__ == "__main__":
    main()

