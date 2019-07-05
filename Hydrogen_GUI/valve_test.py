from H2_components import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
valve1 = Valves('vavle1',11)

while True:
    A = input("1 for LOW, 0 for HIGH")
    print(A)
    if A == '1':
        print("LOW")
        valve1.LOW()
    elif A == '0':
        print("HIGH")
        valve1.HIGH()
    else:
        print('INVALID')
