import RPi.GPIO as GPIO

class lightoff:
    def __init__(self, pin):
        self. pin = pin
    def start(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)    
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.cleanup(self.pin)

