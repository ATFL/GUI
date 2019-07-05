from H2_components import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
valve1 = Valve('vavle1',11)

while True:
    A = input("1 for HIGH, 0 for LOW")
    print(A)
    if A == '1':
        print("LOW")
        valve1.LOW()
    elif A == '0':
        print("HIGH")
        valve1.HIGH()
    else:
        print('INVALID')
