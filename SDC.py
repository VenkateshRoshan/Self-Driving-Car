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

def Forward(co=100) :
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
    print(f'\rMoving Forward','.'*n,'\t',end="")
    
def Backward(co=100) :
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
    
def Left(co=100,c=25) :
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(c)
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(c)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co)
    n = random.randint(0,5)
    print(f'\rTurning Left','.'*n,'\t',end="")
    
def Right(co=100,c=25) :
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(c)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(co)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(c)
    n = random.randint(0,5)
    print(f'\rTurning Left','.'*n,'\t',end="")
    
def MoveForward(co=100) :
    
    
def stop(co=0) :
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(0)
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(0)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(0)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(0)
    print(f'\rStopped',end="\n")
    
def showImg() :
    ret , frame = cam.read()
    frame = cv2.flip(frame,1)
    cv2.imshow('image',frame)
    cv2.waitKey(1)
    
def MeasureDist() :
    
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

def Run_Auto() :
    try :
        print('[*] Motor Started')
        while 1 :
            MoveForward(100)
            time.sleep(2)
            #MoveBackward(100)
            #time.sleep(2)
            #TurnLeft(100)
            stop()
            time.sleep(1)
    except KeyboardInterrupt :
        print('\n')
        stop()
        gpio.cleanup()
        cv2.destroyAllWindows()
        exit()
        
def Run_Manual() :
    try :
        print('[*] Motor Started')
        while 1 :
            #showImg()
            dist = MeasureDist()
            s = input('\n->') + ' '
            if s[0].lower() == 'f' :
                if dist >= 25 :
                    MoveForward(100)
                else :
                    TurnLeft(100)
            else :
                if dist >= 25 :
            if False :
                MoveBackward(100)
                time.sleep(2)
                stop()
            else :
                if s[0].lower() == 'f' :
                    if dist > 20 :
                        MoveForward(100)
                    else :
                        stop()
                elif s[0].lower() == 'b' :
                    if dist > 20 :
                        MoveBackward(100)
                    else :
                        stop()
                elif s[0].lower() == 'l' :
                    TurnLeft(100)
                elif s[0].lower() == 'r' :
                    TurnRight(100)
                else :
                    stop()
    except KeyboardInterrupt :
        print('\n')
        stop()
        gpio.cleanup()
        cv2.destroyAllWindows()
        exit()

if __name__ == "__main__":
    Run_Manual()
    gpio.cleanup()
    exit()
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

def Forward(co=100) :
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
    
def stop(co=0) :
    gpio.output(Mot[0]['I'],False)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[0]['I'],False)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[0]['I'],False)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[0]['I'],False)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)

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
    except KeyboardInterrupt :
        print('\n')
        stop()
        gpio.cleanup()
        cv2.destroyAllWindows()
        exit()

if __name__ == "__main__":
    Run_Manual()
    gpio.cleanup()
    exit()
