from datetime import datetime as dt
from threading import Thread
from time import sleep as delay
from model.LSM303c import LSM303
from model.dto.LSM303Dto import LSM303Dto
from service.MqttClient import Mqtt
from service.CalibrationService import CalibrationService
import asyncio
from service.BLEService import BLEService
from collections import deque

TIME_DIFFERENCE = 60 # sekunde

class Main(Thread):

    validRange = 5
    #connStr = "HostName=AirAnalyzerSensors.azure-devices.net;DeviceId=LSM303c;SharedAccessKey=KWeXDVKTPRmoESeKAy3oa6xe4kXKiRhV8GgHDHD1jpQ="

    def __init__(self, mqtt: Mqtt):
        Thread.__init__(self)
        self.calibrationService = CalibrationService()
        self.queue = deque()
        self.ble = BLEService(self.queue)
        self.lsm = LSM303()
        self.mqtt = mqtt
        self.x = []
        self.y = []
        self.z = []
        self.time = []
        self.counter = []

        self.ble.start()
        self.xArr = []
        self.yArr = []
        self.zArr = []

        self.offsetX = None
        self.offsetY = None
        self.offsetZ = None

        self.scaleX = None
        self.scaleY = None
        self.scaleZ = None
        self.client = None

        self.lastTimeSend = 0

    def run(self):
        self.mqtt.start()
        print("MQTT initialized!")
        while True:
            if len(self.queue) is not 0:
                print("_____________________________________________")
                blmsg = self.queue.popleft()
                for dev in blmsg:
                    print("{}".format(dev.getJson()))
            #msg = self.client.getFromQueue() # for azure
            #print("_____________________________________________")
            msg = self.mqtt.getFromQueue()
            jsonMsg = self.lsm.readMag()
            currentTime = dt.now()
            diff = None
            if self.lastTimeSend != 0:
                diff = currentTime - self.lastTimeSend

            if self.lastTimeSend == 0 or (diff != None and diff.seconds > TIME_DIFFERENCE):
                if jsonMsg is not None:
                    self.mqtt.publish(jsonMsg)
                    self.lastTimeSend = currentTime
            if msg != None:
                print("LSMmain_ {}".format(msg))
                #values = msg # azure
                val: int = 0
                topic, values = msg.split(";")

                if val == "125":
                    self.lsm.configuration1_25()
                if val == "10":
                    self.lsm.configuration10()
                if val == "80":
                    self.lsm.configuration80()
                if values == 'calibrate':
                    self.lsm.startCalibration()
                if values == 'otvoren':
                    self.lsm.setReadingStatus(1)
                if values == 'zatvoren':
                    self.lsm.setReadingStatus(2)
                if values == 'kip':
                    self.lsm.setReadingStatus(3)

            delay(0.5)


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

