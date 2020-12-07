
class Calibration:

    def __init__(self, points, validRange):
        self.numberOfPoints = points
        self.validPoints = 0
        self.validRange = validRange
        self.calibrationDone = False
        self.x = []
        self.y = []
        self.z = []

        self.offsetX = None
        self.offsetY = None
        self.offsetZ = None

        self.offsetAvg = None

        self.scaleX = None
        self.scaleY = None
        self.scaleZ = None


    def calibrate(self, x, y, z):

        if self.validPoints < self.numberOfPoints:
            rawX = int(float(x))
            rawY = int(float(y))
            rawZ = int(float(z))

            if len(self.x) == 0:
                self.x.append(rawX)
                self.y.append(rawY)
                self.z.append(rawZ)
                self.validPoints += 1
            else:
                xValid = True
                yValid = True
                zValid = True
                for p in self.x:
                    if (abs(p - rawX) < self.validRange):
                        xValid = False

                for p in self.y:
                    if (abs(p - rawY) < self.validRange):
                        yValid = False

                for p in self.z:
                    if (abs(p - rawZ) < self.validRange):
                        zValid = False

                if xValid and yValid and zValid:
                    self.x.append(rawX)
                    self.y.append(rawY)
                    self.z.append(rawZ)
                    self.validPoints += 1
                print("_________________Točka: {}".format(self.validPoints))

            return False, x, y, z
        else:
            self.calibrationDone = True
            return True, x, y, z


    def calculateOffset(self):
        self.offsetX = (max(self.x) - min(self.x)) / 2
        self.offsetX = (int(self.offsetX) << 1) & 0xFF
        self.offsetY = (max(self.y) - min(self.y)) / 2
        self.offsetY = (int(self.offsetY) << 1) & 0xFF
        self.offsetZ = (max(self.z) - min(self.z)) / 2
        self.offsetZ = (int(self.offsetZ) << 1) & 0xFF
        self.offsetAvg = (self.offsetX + self.offsetY + self.offsetZ) / 3
        print("Offset:")
        print(self.offsetX)
        print(self.offsetY)
        print(self.offsetZ)
        print(self.offsetAvg)
        print("_____________________________________________")
        return self.offsetX, self.offsetY, self.offsetZ


    def calculateScale(self):
        self.scaleX = self.offsetAvg / self.offsetX
        self.scaleY = self.offsetAvg / self.offsetY
        self.scaleZ = self.offsetAvg / self.offsetZ
        print("Scales:")
        print(self.scaleX)
        print(self.scaleY)
        print(self.scaleZ)
        return self.scaleX, self.scaleY, self.scaleZ

    def setOffset(self, x, y, z):
        self.offsetX = x
        self.offsetY = y
        self.offsetZ = z
        print("Offset set: {}, {}, {}".format(self.offsetX, self.offsetY, self.offsetZ))

    def setScale(self, x, y, z):
        self.scaleX = x
        self.scaleY = y
        self.scaleZ = z
        print("Scale set: {}, {}, {}".format(self.scaleX, self.scaleY, self.scaleZ))

    def calibrateValues(self, x, y, z):
        valid = self.checkCalibration()
        if valid:
            calibrateX = (x - self.offsetX) * self.scaleX
            calibrateY = (y - self.offsetY) * self.scaleY
            calibrateZ = (z - self.offsetZ) * self.scaleZ
            return calibrateX, calibrateY, calibrateZ
        else:
            return x, y, z

    def checkCalibration(self):
        if self.offsetX == None or self.offsetY == None or self.offsetZ == None \
                or self.scaleX == None or self.scaleY == None or self.scaleZ == None:
            return False
        else:
            return True