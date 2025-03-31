#recieve the accelearation info from the accelerometer (x,y,z) 
#calculate current speed ( Vnew = Vold + a * dt) for each direction (x,y,z)
#calculate the magnitude of the speed (V = sqrt(Vx^2 + Vy^2 + Vz^2))
#check if the abs speed is greater than 1.7 m/s, if so, send enable signal to GPS (our enabler is A0/GPIO 26 pin)
#send enable signal to wifi server side, to make sure it only gets updated when EN is on 
# make this an interrupt function, so that it can be called when the accelerometer is updated, have it call the accelerometer every 

from ./accelerometer import *
from ./GPS import *
from machine import Pin
import time



from accelerometer import get_acceleration  
from machine import Pin
import time

def main():
    Vx = 0.0
    Vy = 0.0
    Vz = 0.0
    threshold = 1.7  # m/s
    dt = 0.05  # time interval in seconds (50 ms)
    
    en_pin = Pin(26, Pin.OUT)  # GPIO26 (A0) as GPS enable output

    while True:
        # Get acceleration values (in m/s²)
        ax, ay, az = get_acceleration()

        # Speed integration
        Vx += ax * dt
        Vy += ay * dt
        Vz += az * dt

        # Magnitude of speed vector
        V = (Vx**2 + Vy**2 + Vz**2)**0.5
        print("Current Speed:", V)

        # Enable GPS if speed exceeds threshold
        if V > threshold:
            en_pin.on()
            print("GPS Enabled")
        else:
            en_pin.off()
            print("GPS Disabled")

        time.sleep(dt)

# Start main function
if __name__ == "__main__":
    main()
