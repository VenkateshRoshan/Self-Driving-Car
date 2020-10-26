import RPi.GPIO as gpio
from time import sleep
import time
import random

gpio.setmode(gpio.BOARD)

## output setting

gpio.setup(3,gpio.OUT)
gpio.setup(5,gpio.OUT)
gpio.setup(7,gpio.OUT)

# Motor Running
pwm = gpio.PWM(7,100)
pwm.start(1)
co = 100 # Max - 100 ; Min - 0
def MoveForward(co) :
    gpio.output(3,True)
    gpio.output(5,False)
    print(f'\r[*] Forward {co}\t\t\t',end="")
    pwm.ChangeDutyCycle(co)
    sleep(10)
    
def MoveBackWard(co) :
    gpio.output(5,True)
    gpio.output(3,False)
    print(f'\r[*] Backward {co}\t\t\t',end="")
    pwm.ChangeDutyCycle(co)
    sleep(10)
    
try :
    print('[*] Motor Started')
    while 1 :
        n = random.randint(30,101)
        if n%2 :
            MoveForward(n)
        else :
            MoveBackWard(n)
except KeyboardInterrupt :
    gpio.cleanup()

gpio.cleanup()
exit()