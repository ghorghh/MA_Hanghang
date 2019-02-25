# Class pwm
import time
##import RPi.GPIO as GPIO
import logging
import pigpio

class mypwm:
    def __init__(self, dutycycle, pin, freq, target_brightness, low_brightness,
                 high_brightness, step, rang):
        self.dutyCycle = dutycycle
        self.pin = pin
        self.freq = freq
        self.target_brightness = target_brightness
        self.low_brightness = low_brightness
        self.high_brightness = high_brightness
        self.step = step
        self.rang = rang

    def start(self):

        pwm = pigpio.pi()
        pwm.set_PWM_frequency(self.pin, self.freq)
        pwm.set_PWM_range(self.pin, self.rang)
        pwm.set_PWM_dutycycle(self.pin, self.dutyCycle)
        logging.info("----------------")
        logging.info("Warte auf Helligkeitswert...")
        logging.info("AnfangsdutyCycle ist: {}%".format(self.dutyCycle/self.rang*100))
        logging.info('----------------\n')
        return pwm

    def get_sc_brightness(self, data_struct):
        brightness = data_struct[10]
        return brightness
        
    def pwm_regelung(self,pwm, data_struct):
        brightness = self.get_sc_brightness(data_struct)
        #wenn Deckel nicht gefunden wird
        if data_struct[10] != 0:
            logging.info('Helligkeit ist: {}'.format(brightness))
            if (brightness > (self.target_brightness + self.high_brightness - 4)):
                logging.info("Helligkeit ist: zu hoch")
                if (self.dutyCycle >= self.step):
                    self.dutyCycle = self.dutyCycle - self.step
                    pwm.set_PWM_dutycycle(self.pin, self.dutyCycle)

            elif (brightness < (self.target_brightness - self.low_brightness + 4)):
                logging.info("Helligkeit ist: zu niedrig")
                if (self.dutyCycle <= (self.rang - self.step)):
                    self.dutyCycle = self.dutyCycle + self.step
                    pwm.set_PWM_dutycycle(self.pin, self.dutyCycle)           
            else: # If DutyCycle > (100 - dutyCycleStep) -> no change
                logging.info("Helligkeit ist: gut")
            logging.info('neue DutyCycle: {}%'.format(int(self.dutyCycle/self.rang*100)))
        


    
