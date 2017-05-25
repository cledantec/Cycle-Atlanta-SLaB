import RPi.GPIO as GPIO
import time

trigger = 25
trigger_en = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_en, GPIO.OUT)
GPIO.setup(trigger, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.output(trigger_en, GPIO.HIGH)



while True:
    t = GPIO.input(trigger)
    while not t:
        t = GPIO.input(trigger)
        time.sleep(0.1)
    execfile("/home/pi/testing/i2c.py")
    execfile("/home/pi/testing/serial_read.py")
    time.sleep(4)
