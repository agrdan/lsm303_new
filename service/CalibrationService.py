from utilities.DBUtil import DBUtil
from utilities.Calibration import Calibration
from model.entity.Calibration import Calibration as EntityCalibration
from model.entity.WindowsStatus import WindowsStatus

POINTS = 30
RANGE = 5

class CalibrationService:

    def __init__(self):
        self.calibration = Calibration(POINTS, RANGE)
        cal: EntityCalibration = self.getCalibration()
        self.calibrationStarted = False
        self.calibrationDone = False
        if cal is not None:
            print("Calibracija ucitana")
            self.calibration.setOffset(cal.offset_x, cal.offset_y, cal.offset_z)
            self.calibration.setScale(cal.scale_x, cal.scale_y, cal.scale_z)
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
                print("offsets: {}, {}, {}".format(ox, oy, oz))
                print("scales: {}, {}, {}".format(sx, sy, sz))
                print("_______________________________________________________-")
                entity = EntityCalibration.create(ox, oy, oz, sx, sy, sz)
                print("offsets: {}, {}, {}".format(entity.offset_x, entity.offset_y, entity.offset_z))
                print("scales: {}, {}, {}".format(entity.scale_x, entity.scale_y, entity.scale_z))
                self.insertToDB(entity)
                self.calibrationStarted = False
                print("Calibration done")
            return x, y, z
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

    def setWindowStatus(self, x, y, z, status):
        winStatus = WindowsStatus.create(x, y, z, status)
        entity = DBUtil.findByStatus(WindowsStatus, status)
        if entity is None:
            DBUtil.insert(entity)
        else:
            DBUtil.updateWindowsStatus(WindowsStatus, winStatus)