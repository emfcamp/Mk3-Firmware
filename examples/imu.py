from imu import IMU
import pyb

imu = IMU()

while True:
    print(imu.get_acceleration())
    pyb.delay(1000);
