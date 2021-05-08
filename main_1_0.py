import RPi.GPIO as gpio
from time import sleep
import time
import random
import cv2
import threading


cam = cv2.VideoCapture(0)

gpio.setmode(gpio.BOARD)
TRIG = 29
ECHO = 31
show = False
stopThreads = False
presentState = None
previousState = None
warn = False
dist = 0
carState = 'Not Started'
thread_CamShow = None
thread_DistMeas = None
__Speed__ = 20
gpio.setwarnings(False)
oldRec , newRec = 0 , 0



Mot = [{'P' : 'F_L' , 'I' : 26, 'O' : 24, 'E' : 22},
       {'P' : 'F_R' , 'I' : 40, 'O' : 38, 'E' : 36},
       {'P' : 'B_L' , 'I' : 11, 'O' : 13, 'E' : 15},
       {'P' : 'B_R' , 'I' : 35, 'O' : 37, 'E' : 33}]

for M in Mot :
    for key in M :
        if key != 'P' :
            gpio.setup(M[key],gpio.OUT)

pwm_F_L = gpio.PWM(Mot[0]['E'],100)

pwm_F_L.start(100)

pwm_F_R = gpio.PWM(Mot[1]['E'],100)

pwm_F_R.start(100)

pwm_B_L = gpio.PWM(Mot[2]['E'],100)

pwm_B_L.start(100)

pwm_B_R = gpio.PWM(Mot[3]['E'],100)

pwm_B_R.start(100)

""" Movements    """

"""
    Forward Move activating 'I' and 'O' Activations
"""

def MoveForward(co=10) :
    global presentState
    presentState = 'F'
    gpio.output(Mot[0]['I'],True) # In Activation
    gpio.output(Mot[0]['O'],False) # Out Activation
    pwm_F_L.ChangeDutyCycle(co) # Changing Speed
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(co)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co+10)
    print(f'\r\tMoving Forward\t\t',end="")
    
def stepGear() :
    while True :
        global __Speed__
        __Speed__ = 20
        MoveForward(__Speed__)
        time.sleep(3)
        stop()
    

def stop(co=0) :
    """
        stop
    """
    global presentState
    presentState = 'S'
    gpio.output(Mot[0]['I'],False)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[1]['I'],False)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[2]['I'],False)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(co)
    gpio.output(Mot[3]['I'],False)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co)
    
def Run() :
    while True :
        stepGear()
        exit()
        
if __name__ == "__main__":
    try :
        #thread_CamShow = threading.Thread(target=CamView.show)
        #thread_DistMeas = threading.Thread(target=mov)
        #thread_CamShow.start()
        #thread_DistMeas.start()
        Run()
    except KeyboardInterrupt :
        print('\n\n')
        stopThreads = True
        pwm_F_L.stop()
        pwm_F_R.stop()
        pwm_B_L.stop()
        pwm_B_R.stop()
        stop()
        gpio.cleanup()
        cv2.destroyAllWindows()
    exit()