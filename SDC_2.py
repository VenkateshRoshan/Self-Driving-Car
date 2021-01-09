import RPi.GPIO as gpio
from time import sleep
import time
import random
import cv2

#cam = cv2.VideoCapture(0)

gpio.setmode(gpio.BOARD)

## output setting

M_F_L = 3
M_F_R = 5
E1 = 7

M_B_L = 11
M_B_R = 13
E2 = 15

TRIG = 16
ECHO = 18

gpio.setup(M_F_L,gpio.OUT)
gpio.setup(M_F_R,gpio.OUT)
gpio.setup(E1,gpio.OUT)

gpio.setup(M_B_L,gpio.OUT)
gpio.setup(M_B_R,gpio.OUT)
gpio.setup(E2,gpio.OUT)

# Motor Running
pwm_F = gpio.PWM(E1,100)
pwm_B = gpio.PWM(E2,100)
pwm_F.start(100)
pwm_B.start(100)
co = 100 # Max - 100 ; Min - 0
def MoveForward(co,t=2) :
    gpio.output(M_F_L,True)
    gpio.output(M_F_R,False)
    #print(f'\r[*] Forward \t {co}\t\t',end="")
    pwm_F.ChangeDutyCycle(co)
    gpio.output(M_B_L,True)
    gpio.output(M_B_R,False)
    print(f'\r[*] Forward \t {co}\t\t',end="")
    pwm_B.ChangeDutyCycle(co)
    #sleep(t)
    
def MoveBackWard(co,t=2) :
    gpio.output(M_F_R,True)
    gpio.output(M_F_L,False)
    #print(f'\r[*] Forward \t {co}\t\t',end="")
    pwm_F.ChangeDutyCycle(co)
    gpio.output(M_B_R,True)
    gpio.output(M_B_L,False)
    print(f'\r[*] Backward \t {co}\t\t',end="")
    pwm_B.ChangeDutyCycle(co)
    sleep(t)
    
def TurnLeft(co,t=2) :
    gpio.output(M_F_R,True)
    gpio.output(M_F_L,False)
    #print(f'\r[*] Forward \t {co}\t\t',end="")
    pwm_F.ChangeDutyCycle(co-10)
    gpio.output(M_B_R,True)
    gpio.output(M_B_L,False)
    print(f'\r[*] Left \t {co}\t\t',end="")
    pwm_B.ChangeDutyCycle(co)
    sleep(t)
    
def stop(t=1,co=0) :
    sleep(t)
    pwm_F.ChangeDutyCycle(co)
    pwm_B.ChangeDutyCycle(co)
    print(f'\r[*] Stopped \t {co}\t\t',end="")
    sleep(t)
    
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

def showImg() :
    ret , frame = cam.read()
    frame = cv2.flip(frame,1)
    cv2.imshow('image',frame)
    cv2.waitKey(1)
 
def Run() :
    try :
        print('[*] Motor Started')
        while 1 :
            #showImg()
            dist = MeasureDist()
            """if dist > 30 :
                MoveForward(100)
                #MoveBackWard(100)
            elif 20 < dist <= 30 :
                MoveForward(90)
            elif 5 < dist <= 20 :
                MoveForward(80)
            elif 3 <= dist <= 5 :
                MoveBackWard(100)
            else :
                stop()"""
            i = input('-> : ')
            if i.startswith('f' or 'F') :
                MoveForward(100)
            elif i.startswith('b' or 'B') :
                MoveBackWard(100)
            else :
                stop()
    except KeyboardInterrupt :
        gpio.cleanup()
        cv2.destroyAllWindows()
        exit()

if __name__ == "__main__":
    Run()
    gpio.cleanup()
    exit()

