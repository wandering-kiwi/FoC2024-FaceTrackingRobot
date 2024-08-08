import RPi.GPIO as GPIO
import time

# Control M2 motor
L_IN1 = 20
L_IN2 = 21
L_PWM1 = 0
# Control M1 motor
L_IN3 = 22
L_IN4 = 23
L_PWM2 = 1
# Control M3 motor
R_IN1 = 24
R_IN2 = 25
R_PWM1 = 12
# Control M4 motor
R_IN3 = 26
R_IN4 = 27
R_PWM2 = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # use BCM numbers
#set the MOTOR Driver
GPIO.setup(L_IN1,GPIO.OUT)
GPIO.setup(L_IN2,GPIO.OUT)
GPIO.setup(L_PWM1,GPIO.OUT)
GPIO.setup(L_IN3,GPIO.OUT)
GPIO.setup(L_IN4,GPIO.OUT)
GPIO.setup(L_PWM2,GPIO.OUT)
GPIO.setup(R_IN1,GPIO.OUT)
GPIO.setup(R_IN2,GPIO.OUT)
GPIO.setup(R_PWM1,GPIO.OUT)
GPIO.setup(R_IN3,GPIO.OUT)
GPIO.setup(R_IN4,GPIO.OUT)
GPIO.setup(R_PWM2,GPIO.OUT)
GPIO.output(L_IN1,GPIO.LOW)
GPIO.output(L_IN2,GPIO.LOW)
GPIO.output(L_IN3,GPIO.LOW)
GPIO.output(L_IN4,GPIO.LOW)
GPIO.output(R_IN1,GPIO.LOW)
GPIO.output(R_IN2,GPIO.LOW)
GPIO.output(R_IN3,GPIO.LOW)
GPIO.output(R_IN4,GPIO.LOW)
#set pwm frequence to 1000hz
pwm_R1 = GPIO.PWM(R_PWM1,100)
pwm_R2 = GPIO.PWM(R_PWM2,100)
pwm_L1 = GPIO.PWM(L_PWM1,100)
pwm_L2 = GPIO.PWM(L_PWM2,100)
#set inital duty

pwm_R1.start(0)
pwm_L1.start(0)
pwm_R2.start(0)
pwm_L2.start(0)

def topLeft(speed):
    if speed > 0:
        GPIO.output(L_IN1,GPIO.LOW) #Upper Left forward
        GPIO.output(L_IN2,GPIO.HIGH)
        pwm_L1.ChangeDutyCycle(speed)
    else:
        GPIO.output(L_IN1,GPIO.HIGH) #Upper Left forward
        GPIO.output(L_IN2,GPIO.LOW)
        pwm_L1.ChangeDutyCycle(speed*(-1))
def bottomLeft(speed):
    if speed < 0:
        GPIO.output(L_IN3,GPIO.LOW) #Lower left forward
        GPIO.output(L_IN4,GPIO.HIGH)
        pwm_L2.ChangeDutyCycle(speed*(-1))
    else:
        GPIO.output(L_IN3,GPIO.HIGH) #Lower left forward
        GPIO.output(L_IN4,GPIO.LOW)
        pwm_L2.ChangeDutyCycle(speed)
def topRight(speed):
    if speed < 0:
        GPIO.output(R_IN1,GPIO.LOW) #Upper Right forward
        GPIO.output(R_IN2,GPIO.HIGH)
        pwm_R1.ChangeDutyCycle(speed*(-1))
    else:
        GPIO.output(R_IN1,GPIO.HIGH) #Upper Right forward
        GPIO.output(R_IN2,GPIO.LOW)
        pwm_R1.ChangeDutyCycle(speed)
def bottomRight(speed):
    if speed > 0:
        GPIO.output(R_IN3,GPIO.LOW) #Lower Right forward
        GPIO.output(R_IN4,GPIO.HIGH)
        pwm_R2.ChangeDutyCycle(speed)
    else:
        GPIO.output(R_IN3,GPIO.HIGH) #Lower Right forward
        GPIO.output(R_IN4,GPIO.LOW)
        pwm_R2.ChangeDutyCycle(speed*(-1))

def turnRight(speed):
    topRight(-speed)
    bottomRight(-speed)
    topLeft(speed)
    bottomLeft(speed)
#     time.sleep(0.1)
#     bottomLeft(0)
#     topLeft(0)

def turnLeft(speed):
    topLeft(-speed)
    bottomLeft(-speed)
    topRight(speed)
    bottomRight(speed)
#     time.sleep(0.1)
#     bottomRight(0)
#     topRight(0)
def forward(speed):
    topLeft(speed)
    bottomLeft(speed)
    topRight(speed)
    bottomRight(speed)

def backward(speed):
    topLeft(-speed)
    bottomLeft(-speed)
    topRight(-speed)
    bottomRight(-speed)

def right(speed):
    topLeft(-speed)
    bottomLeft(speed)
    topRight(speed)
    bottomRight(-speed)

def left(speed):
    topLeft(speed)
    bottomLeft(-speed)
    topRight(-speed)
    bottomRight(speed)

def stop():
    #stop pwm
    pwm_R1.stop()
    pwm_L1.stop()
    pwm_R2.stop()
    pwm_L2.stop()
    # GPIO.cleanup() #release all GPIO


speedScale = 1
def mps(vel):
   speedScale = vel
def runMotors(TL, TR, BL, BR):
   # motor stuff here i haven't figured out yet
    topLeft(TL)
    topRight(TR)
    bottomLeft(BL)
    bottomRight(BR)
   # just to get some sort of a result
def moveBySpeeds(left, right, dist, skew=0, maxSpeed=90):
    TL = left - skew
    TR = right + skew
    BR = left + skew
    BL = right - skew
    tempList = [TL, TR, BR, BL]
    # print(tempList)
    otherTempList = []
    for i in tempList:
        if i > maxSpeed:
            i = maxSpeed
            otherTempList.append(i)
        elif i < -maxSpeed:
            i = -maxSpeed
            otherTempList.append(i)
        else:
            otherTempList.append(i)
    # print(otherTempList, maxSpeed)
    TL = otherTempList[0]
    TR = otherTempList[1]
    BR = otherTempList[2]
    BL = otherTempList[3]
    time = dist/speedScale
    runMotors(TL, TR, BL, BR)
def move(x, y, distScale=1, maxSpeed=90, skew=0):
    if x==0 and y==0:
        moveBySpeeds(0, 0, 1, skew=skew, maxSpeed=maxSpeed)
        return
    left = x+y
    right = x-y
    bigger = max(abs(left), abs(right))
    left *= maxSpeed/bigger
    right *= maxSpeed/bigger
    moveBySpeeds(left, right, 1, skew=skew, maxSpeed=maxSpeed)
