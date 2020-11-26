from model.dto.LSM303Dto import LSM303Dto
from service import MqttClient
from time import sleep as delay
from threading import Thread
import json
from datetime import datetime as dt


from service.CalibrationService import CalibrationService
from utilities.SQLite import SQLite
from model.LSM303c import LSM303


class Main(Thread):

    validRange = 5

    def __init__(self, mqtt: MqttClient):
        Thread.__init__(self)
        self.calibrationService = CalibrationService()
        self.lsm = LSM303()
        self.mqtt = mqtt
        self.x = []
        self.y = []
        self.z = []
        self.time = []
        self.counter = []

        self.xArr = []
        self.yArr = []
        self.zArr = []

        self.offsetX = None
        self.offsetY = None
        self.offsetZ = None

        self.scaleX = None
        self.scaleY = None
        self.scaleZ = None

    def run(self):
        self.mqtt.start()
        print("MQTT initialized!")
        i = 1
        validPoints = 0
        calibrate = True
        calibrationDone = False
        #"""
        while True:
            msg = self.mqtt.getFromQueue()
            self.lsm.readMag()
            if msg != None:
                topic, values = msg.split(";")
                timeNow = dt.now().strftime("%H:%M:%S %Y-%m-%d")
                #print("{} | Message received on topic {}".format(timeNow, topic))
                lsmDto = LSM303Dto().serialize(values, ignoreProperties=False)
                #print("{} {} {}".format(lsmDto.x, lsmDto.y, lsmDto.z))
                xRaw = int(float(lsmDto.x))
                yRaw = int(float(lsmDto.y))
                zRaw = int(float(lsmDto.z))
                if topic == 'lsm/configuration':
                    if values == '125':
                        self.lsm.configuration1_25()
                    if values == '10':
                        self.lsm.configuration10()
                    if values == '80':
                        self.lsm.configuration80()
                    if values == 'calibrate':
                        self.lsm.startCalibration()

            delay(0.5)


        #"""
    def appendCSV(self, fileName, *args):
        content = ""
        for a in args:
            content += a + ";"

        f = open(fileName, 'a')
        f.write(content + "\n")
        f.close()

    def writeFile(self, *args):
        content = ""
        for a in args:
            content += str(a) + ";"

        f = open('calibration.txt', 'w')
        f.write(content + "\n")
        f.close()

    def readCSV(self, filename):
        lines = []
        with open(filename, 'r') as f:
            for line in f:
                lines.append(line)
        lineCnt = 1
        for l in lines:
            time, x, y, z, n = l.split(";")
            self.x.append(x)
            self.y.append(y)
            self.z.append(z)
            self.time.append(time)
            self.counter.append(lineCnt)
            lineCnt += 1
        #print(self.x)


if __name__ == '__main__':
    mqtt = MqttClient.Mqtt(MqttClient._topic)
    main = Main(mqtt)
    main.start()