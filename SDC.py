import RPi.GPIO as gpio
from time import sleep
import time
import random
import cv2

cam = cv2.VideoCapture(0)

gpio.setmode(gpio.BOARD)

TRIG = 35
ECHO = 37

Mot = [{'P' : 'F_L' , 'I' : 24, 'O' : 26, 'E' : 22}, # Cement at Pin #6 Blue at Pin #3
       {'P' : 'F_R' , 'I' : 38, 'O' : 40, 'E' : 36}, # orange at Pin #6 brown at Pin #3
       {'P' : 'B_L' , 'I' : 5, 'O' : 7, 'E' : 3}, # violet at Pin #6 white at Pin #3
       {'P' : 'B_R' , 'I' : 13, 'O' : 15, 'E' : 11}] # Red at Pin #6 and Black at Pin #3

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

def MoveForward(co=100) :
    dist = MeasureDist()
    if dist >= 25 :
        gpio.output(Mot[0]['I'],True)
        gpio.output(Mot[0]['O'],False)
        pwm_F_L.ChangeDutyCycle(co)
        gpio.output(Mot[1]['I'],True)
        gpio.output(Mot[1]['O'],False)
        pwm_F_R.ChangeDutyCycle(co)
        gpio.output(Mot[2]['I'],True)
        gpio.output(Mot[2]['O'],False)
        pwm_B_L.ChangeDutyCycle(co)
        gpio.output(Mot[3]['I'],True)
        gpio.output(Mot[3]['O'],False)
        pwm_B_R.ChangeDutyCycle(co)
        n = random.randint(0,5)
        print(f'Moving Forward','.'*n,'\t',end="")
    
def TurnLeft(co=90) :
    c = 30
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(c)
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(c+10)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co+10)
    n = random.randint(0,5)
    print(f'Moving Forward','.'*n,'\t',end="")
    
def TurnRight(co=90) :
    c = 30
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(c)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(co+10)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(c)
    n = random.randint(0,5)
    print(f'Moving Forward','.'*n,'\t',end="")
    
def MoveBackward(co=100) :
    gpio.output(Mot[0]['O'],True)
    gpio.output(Mot[0]['I'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[1]['O'],True)
    gpio.output(Mot[1]['I'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[2]['O'],True)
    gpio.output(Mot[2]['I'],False)
    pwm_B_L.ChangeDutyCycle(co)
    gpio.output(Mot[3]['O'],True)
    gpio.output(Mot[3]['I'],False)
    pwm_B_R.ChangeDutyCycle(co)
    n = random.randint(0,5)
    print(f'\rMoving Backward','.'*n,'\t',end="")
    
def TurnAround_Left(co=100) :
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(40)
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(co-10)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(45)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co)
    print(f'\rTurning Around Left\t',end="")
    
def stop(co=0) :
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

def MeasureDist() :
    """
        Dist Measuring
    """
    gpio.setup(TRIG,gpio.OUT)
    gpio.setup(ECHO,gpio.IN)
    gpio.output(TRIG, False)
    time.sleep(0.5)
    gpio.output(TRIG, True)
    time.sleep(0.00001)
    gpio.output(TRIG, False)
    counter = 0
    new_reading = False
    while gpio.input(ECHO) == 0:
        pulse_start = time.time()

    while gpio.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17165
    distance = round(distance, 1)
    print (f'\r\t\t\t\tDistance:',distance,'cm',end="")
    return distance

def Run_Manual() :
    try :
        print('[*] Motor Started')
        while 1 :
            dist = MeasureDist()
            s = input('\n->') + ' '
            if s[0].lower() == 'f' :
                MoveForward()
            if s[0].lower() == 's' :
                stop()
            if s[0].lower() == 'b' :
                MoveBackward()
            if s[0].lower() == 'l' :
                TurnLeft()
    except KeyboardInterrupt :
        print('\n')
        stop()
        gpio.cleanup()
        cv2.destroyAllWindows()
        exit()

def Run() :
    """while 1 :
        TurnAround_Left()
        sleep(2)
        MoveForward()
        sleep(1)"""
    """while 1 :
        dist = MeasureDist()
        if dist >= 25 :
            MoveForward()
        else :
            stop()
            sleep(2)
            break"""
        
    Run_Manual()

if __name__ == "__main__":
    Run()
    #Run_Manual()
    gpio.cleanup()
    exit()
