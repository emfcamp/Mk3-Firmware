### Author: EMF Badge team
### Description: Allows access to IMU on the TiLDA
### License: MIT

from pyb import I2C
import ustruct

IMU_ADDRESS = 0x6A
IMU_REG_WHO_AM_I = 0x0F
IMU_REG_ACCEL_DATA = 0X28

class IMU:
    """Simple IMU interface

    Usage:
    imu = IMU()
    while True:
        print(imu.get_acceleration())
        pyb.delay(1000);
    """
    def __init__(self):
        self.accuracy = 8

        self.i2c = I2C(3, I2C.MASTER)
        self.i2c.init(I2C.MASTER)

        pyb.delay(20)

        count = 0
        while not self.i2c.is_ready(IMU_ADDRESS):
            pyb.delay(10)
            count += 1
            if count > 100:
                raise IOError("Can't connect to IMU")

        self.self_check()

        settings_acceleration = 0x00 | 0x04 | 0x40 # ToDo: make this configurable
        self.i2c.mem_write(settings_acceleration, IMU_ADDRESS, 0x10)
        # ToDo: Add Gyro

        self.self_check()

    def self_check(self):
        if self.i2c.mem_read(1, IMU_ADDRESS, IMU_REG_WHO_AM_I)[0] != 0x69:
            raise IOError("IMU self check failed")

    def _acceleration_raw_to_float(self, data, offset):
        input = ustruct.unpack_from("h", data, offset)[0];
        return input  * 0.061 * self.accuracy / 1000

    def get_acceleration(self):
        data = self.i2c.mem_read(6, IMU_ADDRESS, IMU_REG_ACCEL_DATA)
        return {
            'x': self._acceleration_raw_to_float(data, 0),
            'y': self._acceleration_raw_to_float(data, 2),
            'z': self._acceleration_raw_to_float(data, 4)
        }

    # ToDo: Add way to de-init i2c
