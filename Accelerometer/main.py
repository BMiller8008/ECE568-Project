# Example code for (GY-521) MPU6050 Accelerometer/Gyro Module
# Write in MicroPython by Warayut Poomiwatracanont JAN 2023

from MPU6050 import MPU6050

from machine import Pin
import time

mpu = MPU6050()

def get_acceleration():
  
    accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    print("x: " + str(aX) + " y: " + str(aY) + " z: " + str(aZ))
    return aX, aY, aZ

    
    
#         # Gyroscope Data
#         gyro = mpu.read_gyro_data()   # read the gyro [deg/s]
#         gX = gyro["x"]
#         gY = gyro["y"]
#         gZ = gyro["z"]
#         print("x:" + str(gX) + " y:" + str(gY) + " z:" + str(gZ))
    
#         # Rough Temperature
#         temp = mpu.read_temperature()   # read the device temperature [degC]
#         # print("Temperature: " + str(temp) + "°C")

#         # G-Force
#         gforce = mpu.read_accel_abs(g=True) # read the absolute acceleration magnitude
#         print("G-Force: " + str(gforce))
            
#         # Time Interval Delay in SECONDS (micropython is weird)
#         time.sleep(1)

# if __name__ == "__main__":
#     main()