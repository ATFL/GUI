# This code is developed to work with the P-Type linear actuator, which uses an internal potentiometer to sense
# actuator position, and the internal motor is controlled accordingly. This code is a modified version of the
# file named H2_components_v2.py, which was developed for use with the R-Type linear actuators.

# -----> RPi Imports <------
import RPi.GPIO as GPIO
#import piplates.DAQC2plate as DAQC2
import time
import os
import Adafruit_ADS1x15


#    def default(self):
#        print('Moving linear actuator to default(center) position.')
#        GPIO.output(self.pinEnable, GPIO.HIGH)
#        self.pwm.ChangeDutyCycle(7)
#        time.sleep(2)
#        GPIO.output(self.pinEnable, GPIO.LOW)
#        self.state = 'default'


class Valve:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def switch(self):
        if self.state == False:
            self.enable()
        elif self.state == True:
            self.disable()

    def enable(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True
        print(self.name + ' enabled.')
        #print("GPIO.LOW")

    def disable(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False
        print(self.name + ' disabled.')
        #print("GPIO.HIGH")

# class Valves:
#     def __init__(self,name,pin):
#         self.name = name
#         self.pin = pin
#         GPIO.setup(self.pin, GPIO.OUT)
#         GPIO.output(self.pin, GPIO.LOW)
#         self.state = False
#
#     def switch(self):
#         if self.state == False:
#             self.HIGH()
#         elif self.state == True:
#             self.LOW()
#
#     def enable(self):
#         GPIO.output(self.pin,GPIO.HIGH)
#         self.state = True
#         print(self.name + ' HIGH.')
#
#     def disable(self):
#         GPIO.output(self.pin,GPIO.LOW)
#         self.state = False
#         print(self.name + ' LOW.')

class MOS:
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
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN))
                                 #/pow(2, 15))*6.144

    def read(self):
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN)/pow(2, 15))*6.144
        return self.conversion_value

    def print(self):
        self.read()
        print("\nReading from MOS: {}".format(self.conversion_value))

class TemperatureSensor():
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
        self.conversion_value = self.adc.read_adc(self.channel,gain=self.GAIN)

    def read(self):
        self.conversion_value = self.adc.read_adc(self.channel,gain=self.GAIN)
        return self.conversion_value

    def print(self):
        self.read()
        print("\nReading from Temperature Sensor: {}".format(self.conversion_value))

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
        self.conversion_value = ((self.adc.read_adc(self.channel,gain=self.GAIN))/pow(2, 15))*6.144

    def read(self):
        self.conversion_value = ((self.adc.read_adc(self.channel,gain=self.GAIN))/pow(2, 15))*6.144
        return self.conversion_value

    def print(self):
        self.read()
        print("\nReading from Linear Actuator Position Sensor: {}".format(self.conversion_value))
        
class Pump:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def switch(self):
        if self.state == False:
            self.enable()
        elif self.state == True:
            self.disable()

    def enable(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True
        print('Pump enabled.')

    def disable(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False
        print('Pump disabled.')

class PressureSensor():
    def __init__(self, adc, channel):

        self.GAIN = 2 / 3
        self.adc = adc
        self.channel = channel
        self.conversion_value = self.adc.read_adc(self.channel,gain=self.GAIN)

    def read(self):
        self.conversion_value = self.adc.read_adc(self.channel,gain=self.GAIN)
        return self.conversion_value

    def print(self):
        self.read()
        print("\nReading from Pressure Sensor: \n{}".format(self.conversion_value))
