import time
import board
import busio
import adafruit_lsm303dlh_mag
import smbus
from model.dto.LSM303Dto import LSM303Dto
import numpy as np
from service.CalibrationService import CalibrationService
import math


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

        self.readingStatus = -1
        self.xStatus = []
        self.yStatus = []
        self.zStatus = []
        self.avg10 = 0
        self.bus = smbus.SMBus(1)
        self.default_setup()
        print("LSM303C I2C initialized")
        self.calibration = CalibrationService()
        self.otvoren = None
        self.zatvoren = None
        self.kip = None
        self.otvoren, self.zatvoren, self.kip = self.calibration.getAllWindowsStatuses()


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
            self.checkReferentPoints(xCal, yCal, zCal)
            status = self.calculateStatus(xCal, yCal, zCal)
            if status == 1:
                print("Prozor je otvoren")
            if status == 2:
                print("Prozor je zatvoren")
            if status == 3:
                print("Prozor je otvoren na kip")
            lsm = LSM303Dto()
            lsm.x = str(xCal)
            lsm.y = str(yCal)
            lsm.z = str(zCal)
            return lsm.getJson()
        else:
            return None

    def startCalibration(self):
        self.calibration.startCalibration()


    def setReadingStatus(self, status):
        self.readingStatus = status


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


    def checkReferentPoints(self, xCal, yCal, zCal):
        if self.readingStatus != -1:
            print("Using window referent points")
            if self.avg10 < 10:
                self.xStatus.append(xCal)
                self.yStatus.append(yCal)
                self.zStatus.append(zCal)
                self.avg10 += 1
            else:
                xAvg = 0
                yAvg = 0
                zAvg = 0
                for i in self.xStatus:
                    xAvg += i

                for i in self.yStatus:
                    yAvg += i

                for i in self.zStatus:
                    zAvg += i

                xAvg /= self.avg10
                yAvg /= self.avg10
                zAvg /= self.avg10
                print(xAvg)
                print(yAvg)
                print(zAvg)

                self.calibration.setWindowStatus(xAvg, yAvg, zAvg, self.readingStatus)
                print("Windows points saved for status {}".format(self.readingStatus))
                self.readingStatus = -1
                self.xStatus = []
                self.yStatus = []
                self.zStatus = []
                self.avg10 = 0

    def calculateStatus(self, x, y, z):
        currentVector = int(math.sqrt(math.pow((x + y + z), 2)))
        zatvorenVector = abs(self.zatvoren.vector - currentVector)
        otvorenVector = abs(self.otvoren.vector - currentVector)
        kipVector = abs(self.kip.vector - currentVector)

        if zatvorenVector < otvorenVector and zatvorenVector < kipVector:
            return 2
        if otvorenVector < zatvorenVector and otvorenVector < kipVector:
            return 1
        if kipVector < zatvorenVector and kipVector < otvorenVector:
            return 3

