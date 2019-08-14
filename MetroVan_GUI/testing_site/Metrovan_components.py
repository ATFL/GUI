
# -----> RPi Imports <------
import RPi.GPIO as GPIO
#import piplates.DAQC2plate as DAQC2
import time
import os
import Adafruit_ADS1x15
import busio
import adafruit_bme280
import adafruit_bme280_76
import digitalio
import adafruit_max31855
import board

class LinearActuator:
    def __init__(self, pinLA,pinEnable):
        self.pinLA = pinLA
        self.pinEnable = pinEnable
        GPIO.setup(self.pinLA, GPIO.OUT)
        GPIO.setup(self.pinEnable, GPIO.OUT)
        GPIO.output(self.pinEnable, GPIO.HIGH)
        self.pwm = GPIO.PWM(pinLA, 50)
        self.pwm.start(7)
        time.sleep(1.5)
        GPIO.output(self.pinEnable, GPIO.LOW)
        self.state = 'default'

    def extend(self):
        print('Extending linear actuator.')
        GPIO.output(self.pinEnable, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(4.8)
        time.sleep(2)
        GPIO.output(self.pinEnable, GPIO.LOW)
        self.state = 'extended'

    def retract(self):
        print('Retracting linear actuator.')
        GPIO.output(self.pinEnable, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(10.2)
        time.sleep(2)
        GPIO.output(self.pinEnable, GPIO.LOW)
        self.state = 'retracted'

    def default(self):
        print('Moving linear actuator to default(center) position.')
        GPIO.output(self.pinEnable, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(7)
        time.sleep(1.5)
        GPIO.output(self.pinEnable, GPIO.LOW)
        self.state = 'default'

    def purge(self):
        print('Moving linear actuator to purging position.')
        GPIO.output(self.pinEnable, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(7)
        time.sleep(1.5)
        GPIO.output(self.pinEnable, GPIO.LOW)
        self.state = 'purge'
    def endLinAc(self):
        self.pwm.stop()
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
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN)/pow(2, 15))*6.144

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

def read_BME(init_name):
   print("\nTemperature: %0.1f C" % init_name.temperature)
   print("Humidity: %0.1f %%" % init_name.humidity)
   print("Pressure: %0.1f hPa" % init_name.pressure)
    
def read_MAX31855(init_name):
    tempC = init_name.temperature
    print("Temperature from MAX31855 Thermocouple Amplifier: %0.1f C" %tempC)

class StepperMotor():
    def __init__(self, direction, step, cw, ccw, spr, mode, res):
        self.direction = direction
        self.step = step
        self.cw = cw
        self.ccw = ccw
        self.spr = spr
        self.mode = mode
        self.res = res
        self.step_count = self.spr*8
        self.delay = .0208/16
        GPIO.setup(self.mode, GPIO.OUT)
        GPIO.setup(self.direction, GPIO.OUT)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.output(self.mode, self.res['1/16'])
        
    
    def retract(self):
        GPIO.output(self.direction, self.cw)
        print("Retracting Stepper Motor")
        for x in range(self.step_count):
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(self.delay)
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(self.delay)
            
    def extend(self): 
        GPIO.output(self.direction, self.ccw) 
        print("Extending Stepper Motor") 
        for x in range(self.step_count): 
            GPIO.output(self.step, GPIO.HIGH) 
            time.sleep(self.delay) 
            GPIO.output(self.step, GPIO.LOW) 
            time.sleep(self.delay) 
            
class Heater(): 
    def __init__(self, heatPin) :
        self.heatPin= heatPin 
        GPIO.setup(self.heatPin, GPIO.OUT) 
        GPIO.output(self.heatPin, GPIO.LOW) 
    def heat(self): 
        print("Heater on") 
        GPIO.output(self.heatPin, GPIO.HIGH) 
    def cool(self): 
        print("Heater off") 
        GPIO.output(self.heatPin, GPIO.LOW) 


    
    
        
    
     