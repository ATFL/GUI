# This code was developed to verify the control of a P-type linear actuator. The code
# will both read from the linear actuator's internal potentiometer and command the actuator
# to retracted and extended states.
# Last edited August 2, 2019
# -----> RPi Imports <------
import RPi.GPIO as GPIO
#import piplates.DAQC2plate as DAQC2
import time
import os
import Adafruit_ADS1x15 as ads

LinActRetract = 15
LinActExtend = 13

GPIO.setmode(GPIO.BOARD)

class PositionSensor():
    def __init__(self, adc, channel):
        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        self.GAIN = 2 / 3
        self.adc = adc
        self.channel = channel
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN)/pow(2, 15))*6.144

    def read(self):
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN)/pow(2, 15))*6.144
        return self.conversion_value

    def print(self):
        self.read()
        print("\nReading from Linear Actuator Position Sensor: {}".format(self.conversion_value))
        
class LinearActuator:
    def __init__(self, LinActRetract,LinActExtend):
        self.LinActRetract = LinActRetract
        self.LinActExtend = LinActExtend
        self.extended_state = 3.8
        self.retracted_state = 1.2
        GPIO.setup(self.LinActRetract, GPIO.OUT)
        GPIO.setup(self.LinActExtend, GPIO.OUT)
        GPIO.output(self.LinActRetract, GPIO.LOW)
        GPIO.output(self.LinActExtend, GPIO.LOW)


    def extend(self):
        print('Extending linear actuator.')
        while (positionSensor.read() < self.extended_state):
            GPIO.output(LinActRetract, GPIO.LOW)
            GPIO.output(LinActExtend, GPIO.HIGH)
        self.state = 'extended'    
        GPIO.output(LinActRetract, GPIO.LOW)
        GPIO.output(LinActExtend, GPIO.LOW)

    def retract(self):
        print('Retracting linear actuator.')
        while (positionSensor.read() > self.retracted_state):
            GPIO.output(LinActRetract, GPIO.HIGH)
            GPIO.output(LinActExtend, GPIO.LOW)
        self.state = 'retracted'
        GPIO.output(LinActRetract, GPIO.LOW)
        GPIO.output(LinActExtend, GPIO.LOW)

#    def default(self):
#        print('Moving linear actuator to default(center) position.')
#        GPIO.output(self.pinEnable, GPIO.HIGH)
#        self.pwm.ChangeDutyCycle(7)
#        time.sleep(2)
#        GPIO.output(self.pinEnable, GPIO.LOW)
#        self.state = 'default'
        

# Analog-Digital Converter
adc = ads.ADS1115(0x48)
# Position sensor
Lin_act_position_channel = 2
positionSensor = PositionSensor(adc, Lin_act_position_channel)
linearActuator = LinearActuator(LinActRetract,LinActExtend)

for i in range (0,5):
    linearActuator.retract()
    positionSensor.print()
    time.sleep(5)
    linearActuator.extend()
    positionSensor.print()
    time.sleep(5)
    
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(LinActRetract, GPIO.OUT)
#GPIO.setup(LinActExtend, GPIO.OUT)
#
#
#for i in range( 0, 3): 
#    print('Retracting linear actuator.')
#    GPIO.output(LinActRetract, GPIO.HIGH)
#    GPIO.output(LinActExtend, GPIO.LOW)
#    time.sleep(0.5)
#    GPIO.output(LinActRetract, GPIO.LOW)
#    GPIO.output(LinActExtend, GPIO.LOW)
#    positionSensor.print()
#    time.sleep(3)
#    
#    print('Extending linear actuator.')
#    GPIO.output(LinActRetract, GPIO.LOW)
#    GPIO.output(LinActExtend, GPIO.HIGH)
#    time.sleep(0.5)
#    GPIO.output(LinActRetract, GPIO.LOW)
#    GPIO.output(LinActExtend, GPIO.LOW)
#    positionSensor.print()
#    time.sleep(3)
    

    

# Two motor control pins on the raspberry pi are board pins 13 and 15
# Potentiometer value is read through the ADC on pin A2