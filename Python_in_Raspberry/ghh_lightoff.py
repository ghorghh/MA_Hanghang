import RPi.GPIO as GPIO
import time
import pigpio
import logging
##from lightoff import lightoff

logging.basicConfig(level = logging.INFO)

pi = pigpio.pi()

pi.set_PWM_frequency(26, 1000)# default 5us sample rate
##print(pi.get_PWM_frequency(26))
pi.set_PWM_range(26, 100)#25 - 40000

##lightoff = lightoff(26)
pi.set_PWM_dutycycle(26, 0)

pi.stop()
##lightoff.start()



