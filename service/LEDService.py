from threading import Thread
from time import sleep as delay
import RPi.GPIO as GPIO
from enum import Enum

class MODS(Enum):
    CALIBRATION = 1
    REFERENT = 2
    NORMAL = 3
    OK = 4
    ERROR = 5

class LEDService(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.redLed = 14
        self.greenLed = 15
        self.blueLed = 18
        self.setup()
        self.mode = 3
        self.lastMode = -1


    def run(self):

        while True:
            if self.mode == MODS.CALIBRATION.value:
                self.ledCalibration()
            elif self.mode == MODS.REFERENT.value:
                self.ledReferentPoints()
            elif self.mode == MODS.NORMAL.value:
                self.normal()
            elif self.mode == MODS.OK.value:
                self.OK()
            elif self.mode == MODS.ERROR.value:
                self.error()


            delay(0.1)

    def checkMode(self):
        if self.mode != self.lastMode:
            self.turnOffAll()
            self.lastMode = self.mode

    def redOn(self):
        GPIO.output(self.redLed, GPIO.HIGH)

    def redOff(self):
        GPIO.output(self.redLed, GPIO.LOW)

    def greenOn(self):
        GPIO.output(self.greenLed, GPIO.HIGH)

    def greenOff(self):
        GPIO.output(self.greenLed, GPIO.LOW)

    def blueOn(self):
        GPIO.output(self.blueLed, GPIO.HIGH)

    def blueOff(self):
        GPIO.output(self.blueLed, GPIO.LOW)

    def turnOffAll(self):
        self.redOff()
        self.blueOff()
        self.greenOff()

    def turnOnAll(self):
        self.redOn()
        self.blueOn()
        self.greenOn()

    def setup(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.redLed, GPIO.OUT)
        GPIO.setup(self.greenLed, GPIO.OUT)
        GPIO.setup(self.blueLed, GPIO.OUT)
        self.redOff()
        self.greenOff()
        self.blueOff()
        print("LED SETUP")

    def setMode(self, mode):
        self.mode = mode
        self.checkMode()

    def ledCalibration(self):
        self.redOn()
        delay(1)
        self.redOff()
        delay(1)


    def ledReferentPoints(self):
        self.blueOn()
        delay(1)
        self.blueOff()
        delay(1)


    def normal(self):
        self.greenOn()
        delay(1)
        self.greenOff()
        delay(1)


    def OK(self):
        self.redOn()
        delay(0.3)
        self.redOff()
        self.greenOn()
        delay(0.3)
        self.greenOff()
        self.blueOn()
        delay(0.3)
        self.blueOff()
        self.greenOn()
        delay(0.3)
        self.greenOff()
        self.redOn()
        delay(0.3)
        self.redOff()
        self.mode = MODS.NORMAL.value
        self.checkMode()


    def error(self):
        self.turnOnAll()
        delay(0.5)
        self.turnOffAll()
        delay(0.5)
        self.turnOnAll()
        delay(0.5)
        self.turnOffAll()
        delay(0.5)
        self.turnOnAll()
        delay(0.5)
        self.turnOffAll()
        self.mode = MODS.NORMAL.value
        self.checkMode()