from threading import Thread
from time import sleep as delay
import RPi.GPIO as GPIO


class LEDService(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.redLed = 14
        self.greenLed = 15
        self.blueLed = 18


    def setup(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.redLed, GPIO.OUT)
        GPIO.setup(self.greenLed, GPIO.OUT)
        GPIO.setup(self.blueLed, GPIO.OUT)

    def run(self):
        counter = 0
        while True:
            if counter % 2 == 0:
                self.ledCalibration()
            elif counter % 3 == 0:
                self.ledReferentPoints()
            else:
                self.normal()
            counter += 1

            delay(0.2)



    def ledCalibration(self):
        GPIO.output(self.redLed, GPIO.HIGH)
        delay(1)
        GPIO.output(self.redLed, GPIO.LOW)
        delay(1)


    def ledReferentPoints(self):
        GPIO.output(self.greenLed, GPIO.HIGH)
        delay(1)
        GPIO.output(self.greenLed, GPIO.LOW)
        delay(1)


    def normal(self):
        GPIO.output(self.blueLed, GPIO.HIGH)
        delay(1)
        GPIO.output(self.blueLed, GPIO.LOW)
        delay(1)


    def OK(self):
        pass