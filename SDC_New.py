import RPi.GPIO as gpio
from time import sleep
import time
import random
import cv2

#cam = cv2.VideoCapture(0)

gpio.setmode(gpio.BOARD)

Mot = [{'P' : 'F_L' , 'I' : 23, 'O' : 21, 'E' : 19}, # Cement at Pin #6 Blue at Pin #3
       {'P' : 'F_R' , 'I' : 38, 'O' : 40, 'E' : 36}, # orange at Pin #6 brown at Pin #3
       {'P' : 'B_L' , 'I' : 10, 'O' : 12, 'E' : 8}, # white at Pin #6 violet at Pin #3
       {'P' : 'B_R' , 'I' : 5, 'O' : 7, 'E' : 3}] # Red at Pin #6 and Black at Pin #3

for M in Mot :
    for key in M :
        if key != 'P' :
            gpio.setup(M[key],gpio.OUT)

pwm_F_L = gpio.PWM(Mot[0]['E'],100)

pwm_F_L.start(1)

pwm_F_R = gpio.PWM(Mot[1]['E'],100)

pwm_F_R.start(1)


pwm_B_L = gpio.PWM(Mot[2]['E'],100)

pwm_B_L.start(1)


pwm_B_R = gpio.PWM(Mot[3]['E'],100)

pwm_B_R.start(1)


def MoveForward(co,t=2) :
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
    print(f'\rMoving Forward',end="")
    
def MoveBackward(co,t=2) :
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
    print(f'\rMoving Backward',end="")

def Run() :
    try :
        print('[*] Motor Started')
        while 1 :
            MoveForward(100)
            #MoveBackward(100)
    except KeyboardInterrupt :
        gpio.cleanup()
        cv2.destroyAllWindows()
        exit()

if __name__ == "__main__":
    Run()
    gpio.cleanup()
    exit()