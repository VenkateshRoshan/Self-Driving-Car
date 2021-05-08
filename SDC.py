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
carState = 'S' # Stopped
state = 'not started'
dist = 0
__Speed__ = 20

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

class CamView :
    
    def show(size=400) :
        pTime = 0 
        try :
            while True :
                cTime = time.time()
                fps = 1/(cTime-pTime)
                pTime = cTime
                ret , frame = cam.read()
                frame = cv2.resize(frame,(size,size))
                frame = cv2.flip(frame,0)
                frame = cv2.putText(frame,"Dist : "+str(dist),(10,30),
                                    cv2.FONT_HERSHEY_SIMPLEX,.5,(255,50,50),
                                    1,cv2.LINE_AA)
                if warn or dist <= 30 :
                    frame = cv2.putText(frame,"WARNING !!!",(20,100),
                                        cv2.FONT_HERSHEY_SIMPLEX,.75,(0,0,200),
                                        2,cv2.LINE_AA)
                frame = cv2.putText(frame," fps : "+str(int(fps)),(310,30),
                                    cv2.FONT_HERSHEY_SIMPLEX,.45,(0,150,0),
                                    1,cv2.LINE_AA)
                cv2.imshow('Car View',frame)
                cv2.waitKey(1)
                if stopThreads :
                    break
        except Exception as e:
            cv2.destroyAllWindows()
            print(e)
            
def slowDown() :
    return
      
def mov() :
    while True :
        global dist
        global presentState
        global warn
        if stopThreads :
            break
        dist = MeasureDist()
        if dist <= 30 and carState != 'B' :
            warn = True
            stop()
        elif dist > 30 :
            warn = False
            if presentState == 'S' and state == 'started' :
                global __Speed__
                __Speed__ = 15
                MoveForward()
            
def ChangeMode() :
    pass

def MoveForward(co=50) :
    """
        Moving Forward
    """
    global presentState
    presentState = 'F'
    if state == 'started' :
        global carState
        carState = 'F'
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
        print(f'\r\tMoving Forward\t\t',end="")
    
def TurnLeft(co=50,c=50) :
    """
        Turning Left
    """
    global presentState
    presentState = 'L'
    global carState
    carState = 'F'
    gpio.output(Mot[1]['I'],True)
    gpio.output(Mot[1]['O'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co)
    gpio.output(Mot[0]['O'],True)
    gpio.output(Mot[0]['I'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(co)
    print(f'\r\tTurn Left\t\t',end="")

def TurnRight(co=50,c=50) :
    """
        Turning Right
    """
    global presentState
    presentState = 'R'
    global carState
    carState = 'F'
    gpio.output(Mot[0]['I'],True)
    gpio.output(Mot[0]['O'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(co)
    gpio.output(Mot[1]['O'],True)
    gpio.output(Mot[1]['I'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co)
    print(f'\r\tTurning Right\t\t',end="")
    
def MoveBackward(co=50) :
    """
        Moving Backward
    """
    global presentState
    presentState = 'B'
    global carState
    carState = 'B'
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
    print(f'\r\tMoving Backward\t\t',end="")

def BackRight(co=50) :
    """
        Moving Backward
    """
    global presentState
    presentState = 'BR'
    global carState
    carState = 'B'
    gpio.output(Mot[0]['O'],True)
    gpio.output(Mot[0]['I'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[1]['O'],True)
    gpio.output(Mot[1]['I'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[2]['O'],True)
    gpio.output(Mot[2]['I'],False)
    pwm_B_L.ChangeDutyCycle(co)
    gpio.output(Mot[3]['I'],True)
    gpio.output(Mot[3]['O'],False)
    pwm_B_R.ChangeDutyCycle(co)
    print(f'\r\tBack Right\t\t',end="")
    
def BackLeft(co=50) :
    """
        Moving Backward
    """
    global presentState
    presentState = 'BL'
    global carState
    carState = 'B'
    gpio.output(Mot[0]['O'],True)
    gpio.output(Mot[0]['I'],False)
    pwm_F_L.ChangeDutyCycle(co)
    gpio.output(Mot[1]['O'],True)
    gpio.output(Mot[1]['I'],False)
    pwm_F_R.ChangeDutyCycle(co)
    gpio.output(Mot[2]['I'],True)
    gpio.output(Mot[2]['O'],False)
    pwm_B_L.ChangeDutyCycle(co)
    gpio.output(Mot[3]['O'],True)
    gpio.output(Mot[3]['I'],False)
    pwm_B_R.ChangeDutyCycle(co)
    print(f'\r\tBack Left\t\t',end="")
    
def TurnAround_Left(t=6.5,co=50) :
    """
        Turn around left
    """
    global presentState
    presentState = 'TL'
    #MoveBackward()
    #sleep(.25)
    MoveForward()
    sleep(.25)
    TurnLeft()
    sleep(t)
    MoveForward()
    sleep(.5)
    TurnLeft()
    
def TurnAround_Right(t=6.5,co=50) :
    """
        Turn around Right
    """
    global presentState
    presentState = 'TR'
    MoveForward()
    sleep(.25)
    TurnRight()
    sleep(t)
    MoveForward()
    sleep(.5)
    TurnRight()

def stop() :
    """
        stop
    """
    co = 0
    global presentState
    presentState = 'S'
    global state
    state = 'not started'
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

def MeasureDist() :
    """
        Dist Measuring...
    """
    gpio.setup(TRIG,gpio.OUT)
    gpio.setup(ECHO,gpio.IN)
    gpio.output(TRIG, False)
    time.sleep(.5)
    gpio.output(TRIG, True)
    time.sleep(0.00001)
    gpio.output(TRIG, False)
    counter = 0
    new_reading = False
    pulse_start , pulse_end = 0 , 0
    while gpio.input(ECHO) == 0:
        pulse_start = time.time()

    while gpio.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    #time.sleep(.25)
    return distance


def AutoMode() :
    """
    code for cam and object detection
    """
    #print('Auto Mode')
    while True :
        TurnAround_Left()
    return None

def ManualMode() :
    """
    Manual Operations
    """
    while True :
        st = input(f'[ F / B / L / R / S / BR / BL / E] ->') + ''
        global state
        state = 'started'
        #state = 'f'
        if st.lower() == 'f' :
            MoveForward(__Speed__)
        elif st.lower() == 'b' :
            MoveBackward(__Speed__)
        elif st.lower() == 'l' :
            TurnLeft(__Speed__)
            #TurnAround_Left(15,5)
        elif st.lower() == 'r' :
            TurnRight(__Speed__)
            #TurnAround_Right(15,5)
        elif st.lower() == 'br' :
            BackRight(__Speed__)
        elif st.lower() == 'bl' :
            BackLeft(__Speed__)
        elif st.lower() == 's' :
            stop()
        elif st.lower() == 'e' :
            return
        else :
            stop()
        #cv2.destroyAllWindows()
    return None

def FixedMode() :
    """
    Fixed operations
    """
    while True :
        MoveForward(20)
        time.sleep(1.5)
        TurnRight(20,10)
        time.sleep(2)
        
    return None

def Run() :
    t1 = threading.Thread(target=CamView.show)
    t2 = threading.Thread(target=mov)
    t1.start()
    t2.start()
    while 1 :
        print('[*] SDC Started')
        #c = input('Choose Mode : (M ["Manual"] / (A ["Auto"]) / (F ("Fixed")) -> ') + '\n'
        c = 'm'
        if c[0].lower() == 'm' :
            ManualMode()
        elif c[0].lower() == 'f' :
            FixedMode()
        elif c[0].lower() == 'a' :
            AutoMode()
        else :
            ManualMode()

if __name__ == "__main__":
    try :
        Run()
    except KeyboardInterrupt :
        stopThreads = True
        pwm_F_L.stop()
        pwm_F_R.stop()
        pwm_B_L.stop()
        pwm_B_R.stop()
        print('Program Destroyed')
        stop()
        cv2.destroyAllWindows()
        exit()
    gpio.cleanup()
    exit()
