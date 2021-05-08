import RPi.GPIO as gpio
import time
import random
from time import sleep

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

class Motor() :
    def __init__ (self,Mot,err=None) :
        self.Mot = Mot
        for M in Mot :
            for key in M :
                if key != 'P' :
                    gpio.setup(M[key],gpio.OUT)
                    
        self.pwm_F_L = gpio.PWM(Mot[0]['E'],100)
        self.pwm_F_R = gpio.PWM(Mot[1]['E'],100)
        self.pwm_B_L = gpio.PWM(Mot[3]['E'],100)
        self.pwm_B_R = gpio.PWM(Mot[2]['E'],100)
        
        self.pwm_F_L.start(0)
        self.pwm_F_R.start(0)
        self.pwm_B_L.start(0)
        self.pwm_B_R.start(0)
        
        self.__speed__ = 0
        self.__error__ = err
        
    def move(self,speed=0.25,turn=0.1,t=1,maxSpeed=100,maxTurn=80) :
        k = maxSpeed
        tu = maxTurn
        speed *= k
        turn *= tu
        print(speed , turn)
        lSpeed = speed - turn
        rSpeed = speed + turn
        
        if lSpeed>k : lSpeed = k
        elif lSpeed<-k : lSpeed = -k
        if rSpeed>k : rSpeed = k
        elif rSpeed<-k : rSpeed = -k
        
        print(lSpeed , rSpeed)
        
        self.pwm_F_L.ChangeDutyCycle(abs(lSpeed))
        self.pwm_F_R.ChangeDutyCycle(abs(rSpeed))
        self.pwm_B_L.ChangeDutyCycle(abs(lSpeed))
        self.pwm_B_R.ChangeDutyCycle(abs(rSpeed))
        if lSpeed>0 :
            gpio.output(self.Mot[0]['I'],gpio.HIGH)
            gpio.output(self.Mot[0]['O'],gpio.LOW)
            gpio.output(self.Mot[2]['I'],gpio.HIGH)
            gpio.output(self.Mot[2]['O'],gpio.LOW)
        else:
            gpio.output(self.Mot[0]['O'],gpio.HIGH)
            gpio.output(self.Mot[0]['I'],gpio.LOW)
            gpio.output(self.Mot[2]['O'],gpio.HIGH)
            gpio.output(self.Mot[2]['I'],gpio.LOW)
        if rSpeed>0 :
            gpio.output(self.Mot[1]['I'],gpio.HIGH)
            gpio.output(self.Mot[1]['O'],gpio.LOW)
            gpio.output(self.Mot[3]['I'],gpio.HIGH)
            gpio.output(self.Mot[3]['O'],gpio.LOW)
        else:
            gpio.output(self.Mot[1]['O'],gpio.HIGH)
            gpio.output(self.Mot[1]['I'],gpio.LOW)
            gpio.output(self.Mot[3]['O'],gpio.HIGH)
            gpio.output(self.Mot[3]['I'],gpio.LOW)
        
        sleep(t)
        
    def stop(self,t=0) :
        self.pwm_F_L.ChangeDutyCycle(0)
        self.pwm_B_L.ChangeDutyCycle(0)
        self.pwm_F_R.ChangeDutyCycle(0)
        self.pwm_B_R.ChangeDutyCycle(0)
        self.mySpeed = 0
        sleep(t)

def main() :
    ### Car Error Hard Surface : Speed = .5 , turn = -.75 then it runs straight (maxS = 75 , maxTurn = 50)
    ### Car Error Soft Surface : Speed = .5 , turn = -.25 then it runs straight (maxS = 75 , maxTurn = 50)
    car.move()
    #car.move(.3,.7,2)
    #car.move(.3,.2,2.5)
    car.stop()

if __name__ == '__main__' :
    Mot = [{'P' : 'F_L' , 'I' : 26, 'O' : 24, 'E' : 22},
           {'P' : 'F_R' , 'I' : 40, 'O' : 38, 'E' : 36},
           {'P' : 'B_L' , 'I' : 35, 'O' : 37, 'E' : 33},
           {'P' : 'B_R' , 'I' : 11, 'O' : 13, 'E' : 15}]
    car = Motor(Mot)
    
    main()
    gpio.cleanup()
