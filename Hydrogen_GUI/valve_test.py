from H2_components import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
valve1 = Valve('vavle1',18)

while True:
    A = input("1 for HIGH, 0 for LOW")
    print(A)
    if A == '1':
        print("LOW")
        valve1.LOW()
    else:
        print("HIGH")
        valve1.HIGH()
