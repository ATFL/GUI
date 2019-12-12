import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
#GPIO.setup(27,GPIO.OUT)

#GPIO.output(27, GPIO.HIGH) 


pwm = GPIO.PWM(12,50)
pwm.start(5)
time.sleep(3)
pwm.ChangeDutyCycle(10)
time.sleep(3)
pwm.stop()

GPIO.cleanup()


