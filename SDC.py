import RPi.GPIO as gpio
from time import sleep
import time
import random
import cv2
import threading

cam = cv2.VideoCapture(0)

gpio.setmode(gpio.BOARD)

TRIG = 35
ECHO = 37
Button = 29
show = False

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

gpio.setup(Button,gpio.IN)

class CamView :
    
    def show() :
        try :
            while True :
                ret , frame = cam.read()
                cv2.imshow('image',frame)
                cv2.waitKey(1)
                global stopThreads
                if stopThreads :
                    break
        except Exception as e:
            cv2.destroyAllWindows()
            print(e)
            
def mov() :
    while True :
        dist = MeasureDist()
        global presentState
        if dist <= 20 and (presentState == 'F' or presentState == 'L' or presentState == 'R') :
            stop()
        global stopThreads
        if stopThreads :
            break

def MoveForward(co=100) :
    """
        Moving Forward
    """
    global presentState
    presentState = 'F'
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
    print(f'\rMoving Forward\t',end="")
    
def TurnLeft(co=100) :
    """
        Turning Left
    """
    global presentState
    presentState = 'L'
    c = 10
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co)
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[2]['O'],True)
    gpio.output(Mot[2]['I'],False)
    pwm_B_L.ChangeDutyCycle(100)
    print(f'\rTurn Left\t',end="")
    
def TurnRight(co=100) :
    """
        Turning Right
    """
    global presentState
    presentState = 'R'
    c = 100
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(co)
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[3]['O'],True)
    gpio.output(Mot[3]['I'],False)
    pwm_B_R.ChangeDutyCycle(c)
    print(f'\rTurn Right\t',end="")
    
def MoveBackward(co=100) :
    """
        Moving Backward
    """
    global presentState
    presentState = 'B'
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
    print(f'\rMoving Backward\t',end="")
    
def TurnAround_Left(co=100) :
    """
        Turn around left
    """
    global presentState
    presentState = 'TL'
    while True :
        MoveForward()
        sleep(1.5)
        TurnLeft()
        sleep(5)
        MoveBackward()
        sleep(.5)
    
def TurnAround_Right(co=100) :
    """
        Turn around Right
    """
    global presentState
    presentState = 'TR'
    while True :
        MoveForward()
        sleep(1.5)
        TurnRight()
        sleep(5)
        MoveBackward()
        sleep(.5)

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

def MeasureDist() :
    """
        Dist Measuring...
    """
    gpio.setup(TRIG,gpio.OUT)
    gpio.setup(ECHO,gpio.IN)
    gpio.output(TRIG, False)
    time.sleep(0.25)
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
    print (f'\r\t\t\tDistance:',distance,'cm',end="")
    return distance

def AutoMode() :
    """
    code for cam and object detection
    """
    print('Auto Mode')
    return None

def ManualMode() :
    """
    Manual Operations
    """
    t = threading.Thread(target=CamView.show)
    t.start()
    t1 = threading.Thread(target=mov)
    t1.start()
    #t.join()
    #t1.join()
    while True :
        state = input(f'[ F / B / L / R / S] ->') + ''
        #dist = MeasureDist()
        if state[0].lower() == 'f' :
            MoveForward()
        elif state[0].lower() == 'b' :
            MoveBackward()
        elif state[0].lower() == 'l' :
            TurnLeft()
        elif state[0].lower() == 'r' :
            TurnRight()
        else :
            stop()
        #cv2.destroyAllWindows()
    return None

def FixedMode() :
    """
    Fixed operations
    """
    while 1 :
        dist = MeasureDist()
        TurnAround_Left(dist)
    return None

def Run() :
    print('[*] SDC Started')
    c = input('Choose Mode : (M ["Manual"] / (A ["Auto"]) / (F ("Fixed")) -> ')
    if c[0].lower() == 'm' :
        ManualMode()
    elif c[0].lower() == 'f' :
        FixedMode()
    elif c[0].lower() == 'a' :
        AutoMode()
    else :
        ManualMode()
        
stopThreads = False
presentState = None

if __name__ == "__main__":
    try :
        #CamView()
        while gpio.input(Button) :
            Run()
    except KeyboardInterrupt :
        stopThreads = True
        stop()
        cv2.destroyAllWindows()
    gpio.cleanup()
    exit()