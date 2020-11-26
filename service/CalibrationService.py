from utilities.DBUtil import DBUtil
from utilities.Calibration import Calibration
from model.entity.Calibration import Calibration as EntityCalibration

POINTS = 90
RANGE = 5

class CalibrationService:

    def __init__(self):
        self.calibration = Calibration(POINTS, RANGE)
        cal: Calibration = self.getCalibration()
        self.calibrationStarted = False
        self.calibrationDone = False
        if cal is not None:
            print("Calibracija ucitana")
            self.calibration.setOffset(cal.offsetX, cal.offsetY, cal.offsetZ)
            self.calibration.setScale(cal.scaleX, cal.scaleY, cal.scaleZ)
        self.calibrationValid = self.calibration.checkCalibration()



    def startCalibration(self):
        self.calibration = Calibration(POINTS, RANGE)
        self.calibrationStarted = True

    def calibrateValues(self, x, y, z):
        if self.calibrationStarted:
            print("Calibration start")
            done, x, y, z = self.calibration.calibrate(x, y, z)
            if done:
                ox, oy, oz = self.calibration.calculateOffset()
                sx, sy, sz = self.calibration.calculateScale()
                entity = EntityCalibration.create(ox, oy, oz, sx, sy, sz)
                self.insertToDB(entity)
                self.calibrationStarted = False
                print("Calibration done")

        else:
            return self.calibration.calibrateValues(x, y, z)



    def insertToDB(self, model):
        inserted = DBUtil.insert(model)
        if inserted:
            print("Calibration saved!")

    def getCalibration(self):
        try:
            calibrationList = DBUtil.findAll(EntityCalibration)
            length = len(calibrationList)
            if length > 0:
                entity = calibrationList[length - 1]
                return entity
            else:
                return None
        except Exception as e:
            print(e)
            return None