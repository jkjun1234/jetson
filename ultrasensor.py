#-*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import os

import naverTTS


tts = naverTTS.NaverTTS(0, 0)
 
#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM)
 
# HC-SR04의 트리거 핀을 GPIO 50번, 에코핀을 GPIO 14번에 연결한다.
GPIO_TRIGGER = 17 # board pin :11 triger, BCM pin 17
GPIO_ECHO = 27    #board pin: 13, BCM pin 27
 
print ("Ultrasonic Distance Measurement")
 
# 초음파를 내보낼 트리거 핀은 출력 모드로, 반사파를 수신할 에코 피은 입력 모드로 설정한다.
GPIO.setup(GPIO_TRIGGER,GPIO.OUT) 
GPIO.setup(GPIO_ECHO,GPIO.IN)

tmpPlayPath = './stop.mp3'

def loop_ultra():
    while True:
        stop = 0
        start = 0
        # 먼저 트리거 핀을 OFF 상태로 유지한다
        GPIO.output(GPIO_TRIGGER, False)
        time.sleep(0.0001)
        print("running loop\n")
 
        # 10us 펄스를 내보낸다. 
        # 파이썬에서 이 펄스는 실제 100us 근처가 될 것이다.
        # 하지만 HC-SR04 센서는 이 오차를 받아준다.
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
 
        # 에코 핀이 ON되는 시점을 시작 시간으로 잡는다.
        while GPIO.input(GPIO_ECHO)==0:
            start = time.time()
 
        # 에코 핀이 다시 OFF되는 시점을 반사파 수신 시간으로 잡는다.
        while GPIO.input(GPIO_ECHO)==1:
            stop = time.time()
 
        # Calculate pulse length
        elapsed = stop-start
 
        # 초음파는 반사파이기 때문에 실제 이동 거리는 2배이다. 따라서 2로 나눈다.
        # 음속은 편의상 340m/s로 계산한다. 현재 온도를 반영해서 보정할 수 있다.
        if (stop and start):
            distance = (elapsed * 34000.0) / 2
            print ("Distance : %.1f cm" % distance)
            #f = open("distance.txt", "w")
            if (distance < 30):
                tts.play("멈춰주세요")
                time.sleep(0.5)
                #return 1
               
                #print("distance <30 \n")
                #GPIO.cleanup()
                #time.sleep(1)
                #continue
                # os.system("python myprj.py")
                # f = open("getLabelsPotions.txt", "r")     ##open Labels file
                # data = f.read()
                # data.strip()
                # tts.play(data)
            # else : 
            #     data = '0'
            #     f.write(data)
            # f.close()

def main():
    loop_ultra()
    a=1
    while(a):
        a = loop_ultra()
        print("loop start")

if __name__ == '__main__':
    main()

# try :
# except KeyboardInterrupt:   
#     print ("Ultrasonic Distance Measurement End")
#     #f.close()
#     GPIO.cleanup()
 
 
# Reset GPIO settings
GPIO.cleanup()