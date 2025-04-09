#recieve the accelearation info from the accelerometer (x,y,z) 
#calculate current speed ( Vnew = Vold + a * dt) for each direction (x,y,z)
#calculate the magnitude of the speed (V = sqrt(Vx^2 + Vy^2 + Vz^2))
#check if the abs speed is greater than 1.7 m/s, if so, send enable signal to GPS (our enabler is A0/GPIO 26 pin)
#send enable signal to wifi server side, to make sure it only gets updated when EN is on 
# make this an interrupt function, so that it can be called when the accelerometer is updated, have it call the accelerometer every 

from machine import UART, Pin
from micropyGPS import MicropyGPS
from accelerometer import get_acceleration  
from machine import Pin
import time


def main():
    
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
