import RPi.GPIO as GPIO
import time
import numpy as np
from pathlib import Path
import datetime
import os
import Adafruit_ADS1x15 as ads


valve_1 = 12
valve_2 = 22
valve_3 = 16
valve_4 = 18
valve_5 = 36
valve_6 = 40

# Pin Definitions:
compressed_air_valve = valve_5
chamber_venting_valve = valve_6
mfc1_output_to_chamber_valve = valve_1
mfc2_output_to_chamber_valve = valve_2
mfc1_venting_valve = valve_3
mfc2_venting_valve = valve_4

linear_actuator_extend = 13
linear_actuator_retract = 15


GPIO.setmode(GPIO.BOARD)    # There are two options for this, but just use the board one for now. Don't worry much about it, we can check the definitions when I get back
GPIO.setup(compressed_air_valve, GPIO.OUT) # Specifies mfc_output_to_chamber_valve pin as an output
GPIO.setup(chamber_venting_valve, GPIO.OUT) # Specifies linear_actuator_extend pin as an output
GPIO.setup(mfc1_output_to_chamber_valve, GPIO.OUT) # Specifies linear_actuator_retract pin as an output
GPIO.setup(mfc2_output_to_chamber_valve, GPIO.OUT) # Specifies compressed_air_valve pin as an output
GPIO.setup(mfc1_venting_valve, GPIO.OUT) # Specifies chamber_venting_valve pin as an output
GPIO.setup(mfc2_venting_valve, GPIO.OUT) # Specifies mfc_venting_valve pin as an output
GPIO.setup(linear_actuator_retract, GPIO.OUT) # Specifies chamber_venting_valve pin as an output
GPIO.setup(linear_actuator_extend, GPIO.OUT) # Specifies mfc_venting_valve pin as an output

# Initial state for outputs:
GPIO.output(compressed_air_valve, GPIO.LOW)
GPIO.output(chamber_venting_valve, GPIO.LOW)
GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
GPIO.output(mfc1_venting_valve, GPIO.LOW)
GPIO.output(mfc2_venting_valve, GPIO.LOW)

linear_actuator_extend = 13
linear_actuator_retract = 15

time.sleep(1)

GPIO.output(mfc1_venting_valve, GPIO.HIGH)

time.sleep(10)

GPIO.output(mfc1_venting_valve, GPIO.LOW)

GPIO.output(mfc1_output_to_chamber_valve, GPIO.HIGH)

time.sleep(8)

GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)

GPIO.cleanup()