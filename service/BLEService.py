from threading import Thread
from bluepy.btle import Scanner
from time import sleep as delay
from model.dto.BLEDeviceDto import BLEDeviceDto
from collections import deque


class BLEService(Thread):

    def __init__(self, q):
        Thread.__init__(self)
        self.scanner = Scanner()
        self.queue = q
        self.devicesScanned = []

    def run(self):
        print("Starting BLE service...")
        self.scanner.start()
        while True:
            self.devicesScanned.clear()
            self.scanner.clear()
            self.scanner.process(5.0)
            devices = self.scanner.getDevices()
            self.fillQueue(devices)
            #if len(self.queue) > 0:
            #test = self.getFromQueue()
            #for dev in test:
            #    print("DEV: {}".format(dev.getJson()))
            #    print("_________________________")
            print("_____________________Save ble setup, queue size = {}".format(len(self.queue)))
            delay(3)

    def fillQueue(self, devices):
        for d in devices:
            devDto = BLEDeviceDto(d.addr, d.addrType, d.rssi, d.getScanData())
            self.devicesScanned.append(devDto)
        self.queue.append(self.devicesScanned)

    def getFromQueue(self):
        if len(self.queue) is not 0:
            msg = self.queue.popleft()
            return msg
        else:
            return None
