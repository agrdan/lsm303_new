import time
import board
import busio
import adafruit_lsm303dlh_mag
import smbus
from model.dto.LSM303Dto import LSM303Dto
import numpy as np
from service.CalibrationService import CalibrationService


class Registers:
    LSM = 0x1E
    CTRL_REG1 = 0x20
    CTRL_REG2 = 0x21
    CTRL_REG3 = 0x22
    CTRL_REG4 = 0x23
    CTRL_REG5 = 0x24

    XL = 0x28
    XH = 0x29
    YL = 0x2A
    YH = 0x2B
    ZL = 0x2C
    ZH = 0x2D

    TEMP_L = 0x2E
    TEMP_H = 0x2F

class LSM303:

    def __init__(self):
        #self.i2c = busio.I2C(board.SCL, board.SDA)
        #self.sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(self.i2c)
        self.oldX = None
        self.oldY = None
        self.oldZ = None
        self.bus = smbus.SMBus(1)
        self.default_setup()
        print("LSM303C I2C initialized")
        self.calibration = CalibrationService()


    def default_setup(self):
        self.configuration1_25()
        self.bus.write_byte_data(Registers.LSM, Registers.CTRL_REG3, 0x00)
        self.bus.write_byte_data(Registers.LSM, Registers.CTRL_REG5, 0x00)
        self.bus.write_byte_data(Registers.LSM, Registers.CTRL_REG2, 0x60)

    def read_data(self):
        pass
        #mag_x, mag_y, mag_z = self.sensor.magnetic
        #lsm = LSM303Dto(mag_x, mag_y, mag_z)
        # return lsm.getJson()

    def readMag(self):
        xh = self.bus.read_byte_data(Registers.LSM, Registers.XH)
        xl = self.bus.read_byte_data(Registers.LSM, Registers.XL)
        yl = self.bus.read_byte_data(Registers.LSM, Registers.YL)
        yh = self.bus.read_byte_data(Registers.LSM, Registers.YH)
        zl = self.bus.read_byte_data(Registers.LSM, Registers.ZL)
        zh = self.bus.read_byte_data(Registers.LSM, Registers.ZH)

        x = (np.int16)(int(xh) << 8) | int(xl)
        y = (np.int16)(int(yh) << 8) | int(yl)
        z = (np.int16)(int(zh) << 8) | int(zl)
        if self.oldX != x or self.oldY != y or self.oldZ != z:
            self.oldX = x
            self.oldY = y
            self.oldZ = z
            print("{}, {}, {}".format(x, y, z))

            xCal, yCal, zCal = self.calibration.calibrateValues(int(x), int(y), int(z))
            lsm = LSM303Dto()
            lsm.x = str(xCal)
            lsm.y = str(yCal)
            lsm.z = str(zCal)

            return lsm.getJson()
        else:
            return None

    def startCalibration(self):
        self.calibration.startCalibration()

    def configuration1_25(self):
        self.bus.write_byte_data(Registers.LSM, Registers.CTRL_REG1, 0xC4)
        val = self.bus.read_byte_data(Registers.LSM, Registers.CTRL_REG1)
        if val is 0xC4:
            return True
        else:
            return False


    def configuration10(self):
        self.bus.write_byte_data(Registers.LSM, Registers.CTRL_REG1, 0x28)
        val = self.bus.read_byte_data(Registers.LSM, Registers.CTRL_REG1)
        if val is 0x28:
            return True
        else:
            return False

    def configuration80(self):
        self.bus.write_byte_data(Registers.LSM, Registers.CTRL_REG1, 0x2E)
        val = self.bus.read_byte_data(Registers.LSM, Registers.CTRL_REG1)
        if val is 0x2E:
            return True
        else:
            return False

