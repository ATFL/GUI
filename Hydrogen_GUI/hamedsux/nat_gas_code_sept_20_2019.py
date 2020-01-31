#   This program is designed to automate the data collection process for the ATFL HETEK Project.
#   Developed by Matthew Barriault and Isaac Alexander


# Imports
import RPi.GPIO as GPIO
import time
import numpy as np
from pathlib import Path
import datetime
import os
import Adafruit_ADS1x15 as ads



#------------------------Set up test list every day------------------------#
#methaneConcList = [2150,1750, 165, 1550, 320, 1450, 195, 1250, 637, 2250, 746, 2350, 357, 2000, 558,2200]
#ethaneConcList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# methaneConcList = [300,300,650,200,800,50,1000,700,100,850,950,150,750,250,350,600,900,450,400,500,550]
# ethaneConcList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#methaneConcList = [200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000]
#ethaneConcList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#methaneConcList = [562,1562,628,1628,694,1694,760,1760,826,1826,992,1992]
#ethaneConcList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#methaneConcList = [0,0,1000,970]
#ethaneConcList = [100,100,0,30]
#methaneConcList = [2465,2515,2565,2615,2665,2715,2765,2815,2865]
#ethaneConcList = [0,0,0,0,0,0,0,0,0]

#0% - train
#methaneConcList = [100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000]
#ethaneConcList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#0% - test
#methaneConcList = [813,525,1034,676,1984,2857,833,2657,2448,2164,1316,2570,1346,225,151,553,357,1395,2797,2281,2637,2056,2707,2155,2917,1162,2532,1348,1573,811]
#ethaneConcList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


# 1% - train
#methaneConcList = [99,198,297,396,495,594,693,792,891,990,1089,1188,1287,1386,1485,1584,1683,1782,1881,1980,2079,2178,2277,2376,2475,2574,2673,2772,2871,2970]
#ethaneConcList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
# 1% - test
#methaneConcList = [805,520,1024,669,1964,2828,825,2630,2424,2142,1303,2544,1333,223,149,547,353,1381,2769,2258,2611,2035,2680,2133,2888,1150,2507,1335,1557,803]
#ethaneConcList = [8,5,10,7,20,29,8,27,24,22,13,26,13,2,2,6,4,14,28,23,26,21,27,22,29,17,25,13,16,8]


# 3% - train
#methaneConcList = [97,194,291,388,485,582,679,776,873,970,1067,1164,1261,1358,1455,1552,1649,1746,1843,1940,2037,2134,2231,2328,2425,2522,2619,2716,2813,2910]
#ethaneConcList = [3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81,84,87,90]
# 3% - test
#methaneConcList = [789,509,1003,656,1924,2771,808,2577,2375,2099,1277,2493,1306,218,146,536,346,1353,2713,2213,2558,1994,2626,2090,2829,1127,2456,1308,1526,787]
#ethaneConcList = [24,16,31,20,60,86,25,80,73,65,39,77,40,7,5,17,11,42,84,68,79,62,81,65,88,35,76,40,47,24]


# 5% - train
#methaneConcList = [95,190,285,380,475,570,665,760,855,950,1045,1140,1235,1330,1425,1520,1615,1710,1805,1900,1995,2090,2185,2280,2375,2470,2565,2660,2755,2850]
#ethaneConcList = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150]
# 5% - test
#methaneConcList = [772,499,982,642,1885,2714,791,2524,2326,2056,1250,2442,1279,214,143,525,339,1325,2657,2167,2505,1953,2572,2047,2771,1104,2405,1281,1494,770]
#ethaneConcList = [41,26,52,34,99,143,42,133,122,108,66,129,67,11,8,28,18,70,140,114,132,103,135,108,146,58,127,67,79,41]


# 5% - all
#methaneConcList = [0,0,95,190,285,380,475,570,665,760,855,950,1045,1140,1235,1330,1425,1520,1615,1710,1805,1900,1995,2090,2185,2280,2375,2470,2565,2660,2755,2850,772,499,982,642,1885,2714,791,2524,2326,2056,1250,2442,1279,214,143,525,339,1325,2657,2167,2505,1953,2572,2047,2771,1104,2405,1281,1494,770]
#ethaneConcList = [100,100,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,41,26,52,34,99,143,42,133,122,108,66,129,67,11,8,28,18,70,140,114,132,103,135,108,146,58,127,67,79,41]

# 3% - all
#methaneConcList = [1000,97,194,291,388,485,582,679,776,873,970,1067,1164,1261,1358,1455,1552,1649,1746,1843,1940,2037,2134,2231,2328,2425,2522,2619,2716,2813,2910,789,509,1003,656,1924,2771,808,2577,2375,2099,1277,2493,1306,218,146,536,346,1353,2713,2213,2558,1994,2626,2090,2829,1127,2456,1308,1526,787,1000]
#ethaneConcList = [100,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81,84,87,90,24,16,31,20,60,86,25,80,73,65,39,77,40,7,5,17,11,42,84,68,79,62,81,65,88,35,76,40,47,24,100]

# 1% - all
#methaneConcList = [787,99,198,297,396,495,594,693,792,891,990,1089,1188,1287,1386,1485,1584,1683,1782,1881,1980,2079,2178,2277,2376,2475,2574,2673,2772,2871,2970,805,520,1024,669,1964,2828,825,2630,2424,2142,1303,2544,1333,223,149,547,353,1381,2769,2258,2611,2035,2680,2133,2888,1150,2507,1335,1557,803]
#ethaneConcList = [24,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,8,5,10,7,20,29,8,27,24,22,13,26,13,2,2,6,4,14,28,23,26,21,27,22,29,17,25,13,16,8]


methaneConcList = [100,75,125,175,225,275,325,375,425,475,525,575,625,675,725,775,825,875,925]
ethaneConcList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


if len(methaneConcList) != len(ethaneConcList):
    print ("Error! Concentration lists are not the same length!")

numtests = len(methaneConcList)

#------------------------Variable Declarations------------------------#

sensor_input_channel = 3 # The physical terminal on DAQCplate the sensor number 1 signal is connected to
linear_actuator_position_channel = 2 # The physical terminal on DAQCplate the linear actuator position sensor signal is connected to

adc = ads.ADS1115(0x48)
gain = 2/3

# Following correction factors were provided by MKS (MFC Manufacturer) (Ph. 978-284-4000)
#methane_correction_factor = 0.72 # Manufacturer specified 10 SCCM Nitrogen is equivalent to 7.2 SCCM Methane through the MFC
methane_correction_factor = 0.72
#ethane_correction_factor = 1.01
ethane_correction_factor = 0.5 # Manufacturer specified 10 SCCM Nitrogen is equivalent to 5 SCCM Ethane through the MFC

methane_flow_rate = 10  # mL/min, this will be the arbitrary, constant setpoint of the MFC
ethane_flow_rate = 1
# methane_flow_rate = 1
# ethane_flow_rate = 0.1
diffusion_time = 0 # time allowed for injected gas to diffuse in sensing chamber before sensor exposure occurs
mfc_flow_stabilization_time = 10 # venting flow through MFC for 5 seconds while flow stabilizes. Stable flow is then switch into chamber
switching_time = 1 # time allowed for flow and pressure to stabilize within system while switching purge solenoids
#sensing_delay_time = 130 # time delay after beginning data acquisition till when the sensor is exposed to sample
#sensing_retract_time = 180 # time allowed before sensor is retracted, no longer exposed to sample
#compressed_air_flush_time = 45 # time allowed for compressed air flushing of sensing chamber in seconds
#duration_of_signal = 210 # time allowed for data acquisition per test run
#sensing_delay_time = 300 # time delay after beginning data acquisition till when the sensor is exposed to sample
#sensing_retract_time = 341 # time allowed before sensor is retracted, no longer exposed to sample
#compressed_air_flush_time = 230 # time allowed for compressed air flushing of sensing chamber in seconds
#duration_of_signal = 491 # time allowed for data acquisition per test run
sensing_delay_time = 20 # time delay after beginning data acquisition till when the sensor is exposed to sample
sensing_retract_time = 500 # time allowed before sensor is retracted, no longer exposed to sample
compressed_air_flush_time = 5 # time allowed for compressed air flushing of sensing chamber in seconds
duration_of_signal = 590 # time allowed for data acquisition per test run
extended_state = 4.0 # voltage value achieved when li near actuator is extended to correct sensing depth
retracted_state = 2.6 # voltage value achieved when linear actuator is retracted to idle state
sampling_time = 0.1 # time between samples taken, determines sampling frequency
printing_time = 1
p = True

#------------------------Pin definitions------------------------#

# Pin definitions are BCM
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

#---------------------------------------------------------------------#

# Pin Setup:
GPIO.setmode(GPIO.BOARD)    # There are two options for this, but just use the board one for now. Don't worry much about it, we can check the definitions when I get back
GPIO.setup(compressed_air_valve, GPIO.OUT) # Specifies mfc_output_to_chamber_valve pin as an output
GPIO.setup(chamber_venting_valve, GPIO.OUT) # Specifies linear_actuator_extend pin as an output
GPIO.setup(mfc1_output_to_chamber_valve, GPIO.OUT) # Specifies linear_actuator_retract pin as an output
GPIO.setup(mfc2_output_to_chamber_valve, GPIO.OUT) # Specifies compressed_air_valve pin as an output
GPIO.setup(mfc1_venting_valve, GPIO.OUT) # Specifies chamber_venting_valve pin as an output
GPIO.setup(mfc2_venting_valve, GPIO.OUT) # Specifies mfc_venting_valve pin as an output
GPIO.setup(
    linear_actuator_retract, GPIO.OUT) # Specifies chamber_venting_valve pin as an output
GPIO.setup(linear_actuator_extend, GPIO.OUT) # Specifies mfc_venting_valve pin as an output

# Initial state for outputs:
GPIO.output(compressed_air_valve, GPIO.LOW)
GPIO.output(chamber_venting_valve, GPIO.LOW)
GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
GPIO.output(mfc1_venting_valve, GPIO.LOW)
GPIO.output(mfc2_venting_valve, GPIO.LOW)


#------------------------Function definitions------------------------#

def read_position():
    position = adc.read_adc(linear_actuator_position_channel,gain=gain)/pow(2, 15)*6.144
    return position

def read_mos():
    mos = adc.read_adc(sensor_input_channel,gain=gain)/pow(2, 15)*6.144
    return mos

def read_0():
    val = adc.read_adc(0,gain=gain)/pow(2, 15)*6.144
    return val

def read_1():
    val = adc.read_adc(1,gain=gain)/pow(2, 15)*6.144
    return val

def exposeAndCollectData():

    GPIO.output(compressed_air_valve, GPIO.LOW)
    GPIO.output(chamber_venting_valve, GPIO.LOW)
    GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
    GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
    GPIO.output(mfc1_venting_valve, GPIO.LOW)
    GPIO.output(mfc2_venting_valve, GPIO.LOW)

    start_time = time.time() # capture the time at which the test began. All time values can use start_time as a reference
    dataVector1 = [] # data values to be returned from sensor 1
    dataVector2 = [] # data values to be returned from sensor 2
    dataVector3 = []    
    tempDataVector = []
    humidityDataVector = []
    timeVector = [] # time values associated with data values
    sampling_time_index = 1 #sampling_time_index is used to ensure that sampling takes place every interval of sampling_time, without drifting.
    data_date_and_time = time.asctime( time.localtime(time.time()) ) 
    print("Starting data capture")
            
    while (time.time() < (start_time + duration_of_signal)): # While time is less than duration of logged file


        if (time.time() > (start_time + (sampling_time * sampling_time_index))): # if time since last sample is more than the sampling time, take another sample
                    dataVector1.append( read_mos() ) # Perform analog to digital function, reading voltage from first sensor channel
                    dataVector2.append( read_1() ) #  Perform analog to digital function, reading voltage from second sensor channel
                    dataVector3.append( read_0() )

                    timeVector.append( time.time() - start_time )
                    sampling_time_index += 1 # increment sampling_time_index to set awaited time for next data sample
                    if ((sampling_time_index - 1) % 10 == 0):
                        print(int(time.time() - start_time))

        # If time is between 10-50 seconds and the Linear Actuator position sensor signal from DAQCplate indicates a retracted state, extend the sensor
        #elif (time.time() >= (start_time + sensing_delay_time) and time.time() <= (sensing_retract_time + start_time) and read_position() < extended_state):
        elif (time.time() >= (start_time + sensing_delay_time) and time.time() <= (start_time + sensing_delay_time + 6)):
            GPIO.output(linear_actuator_extend, GPIO.HIGH) # Actuate linear actuator to extended position
            GPIO.output(linear_actuator_retract, GPIO.LOW)# Energizing both control wires causes linear actuator to extend
            print(read_position())

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from DAQCplate indicates an extended state, retract the sensor
        #elif ( ((time.time() < (sensing_delay_time + start_time)) or (time.time() > (sensing_retract_time + start_time)) ) and read_position() > retracted_state):
        elif ( (time.time() > (sensing_retract_time + start_time) and time.time() < (sensing_retract_time + start_time + 0.6)) ):
                                                                                     
            GPIO.output(linear_actuator_retract, GPIO.HIGH) # Retract linear actuator to initial position. Energizing only the linear_actuator_retract wire causes the lineaer actuator to retract
            GPIO.output(linear_actuator_extend, GPIO.LOW)

        # Otherwise, keep outputs off
        else:
            GPIO.output(linear_actuator_retract, GPIO.LOW)
            GPIO.output(linear_actuator_extend, GPIO.LOW)

#   return dataVector1, timeVector
    return dataVector1, dataVector2, dataVector3, timeVector


def inject_methane(injection_conc):
    print('Injecting methane')
    injection_amount = injection_conc / 500 # mL
    injection_time = ( 60 * ( 1 / methane_correction_factor ) * injection_amount ) / methane_flow_rate  # Time in seconds
    print ("Methane injection time is " + str(float(injection_time)))

    # The "try" and "except" statements dictate what the program does if an error occurs
    try:
        # Initial state for outputs:
        GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
        GPIO.output(mfc1_venting_valve, GPIO.LOW)

        # Methane Gas injection:
        GPIO.output(mfc1_venting_valve, GPIO.HIGH) # Open solenoid valve venting flow from the MFC to atmosphere
        print(" mfc1_venting_valve on")

        time.sleep(mfc_flow_stabilization_time) # Vent flow through MFC to stablize flow rate

        GPIO.output(mfc1_output_to_chamber_valve, GPIO.HIGH) # Open solenoid valve controlling flow from MFC into chamber
        print(" mfc1_output_to_chamber_valve on")
        GPIO.output(mfc1_venting_valve, GPIO.LOW) # Close solenoid valve venting flow from MFC to atmosphere
        print(" mfc1_venting_valve off")

        time.sleep(injection_time) # Wait for appropriate injection time

        GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW) # Close solenoid valve controlling flow from MFC into chamber
        print(" mfc1_output_to_chamber_valve off")
        
    except: # This is what happens if any errors occur:
        print("Something's wrong!")


def inject_ethane(injection_conc):
    print('Injecting ethane')
    injection_amount = injection_conc / 500 # mL
    injection_time = ( 60 * ( 1 / ethane_correction_factor ) * injection_amount ) / ethane_flow_rate  # Time in seconds
    print ("Ethane injection time is " + str(float(injection_time)))

    # The "try" and "except" statements dictate what the program does if an error occurs
    try:
            # Initial state for outputs:
                GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
                GPIO.output(mfc2_venting_valve, GPIO.LOW)

                # Ethane Gas injection:

                GPIO.output(mfc2_venting_valve, GPIO.HIGH) # Open solenoid valve venting flow from the MFC to atmosphere
                print(" mfc2_venting_valve on")

                time.sleep(mfc_flow_stabilization_time) # Vent flow through MFC to stablize flow rate

                GPIO.output(mfc2_output_to_chamber_valve, GPIO.HIGH) # Open solenoid valve controlling flow from MFC into chamber
                print(" mfc2_output_to_chamber_valve on")
                GPIO.output(mfc2_venting_valve, GPIO.LOW) # Close solenoid valve venting flow from MFC to atmosphere
                print(" mfc2_venting_valve off")

                time.sleep(injection_time) # Wait for appropriate injection time

                GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW) # Close solenoid valve controlling flow from MFC into chamber
                print(" mfc2_output_to_chamber_valve off")

    except: # This is what happens if any errors occur:
        print("Something's wrong!")


def inject_methane_and_ethane(methane_injection_conc, ethane_injection_conc):
    print('Injecting methane and ethane')
    methane_injection_amount = methane_injection_conc / 500 # mL
    ethane_injection_amount = ethane_injection_conc / 500 # mL

    methane_injection_time = ( 60 * ( 1 / methane_correction_factor ) * methane_injection_amount ) / methane_flow_rate  # Time in seconds
    ethane_injection_time = ( 60 * ( 1 / ethane_correction_factor ) * ethane_injection_amount ) / ethane_flow_rate  # Time in seconds

    print ("Methane injection time is " + str(int(methane_injection_time)))
    print ("Ethane injection time is " + str(int(ethane_injection_time)))

    # The "try" and "except" statements dictate what the program does if an error occurs
    try:
        # Initial state for outputs:
        GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
        GPIO.output(mfc1_venting_valve, GPIO.LOW)
        GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
        GPIO.output(mfc2_venting_valve, GPIO.LOW)

        # Methane Gas injection:
        GPIO.output(mfc1_venting_valve, GPIO.HIGH) # Open solenoid valve venting flow from the MFC to atmosphere
        print(" mfc1_venting_valve on")
        GPIO.output(mfc2_venting_valve, GPIO.HIGH) # Open solenoid valve venting flow from the MFC to atmosphere
        print(" mfc2_venting_valve on")

        time.sleep(mfc_flow_stabilization_time) # Vent flow through MFC to stablize flow rate

        GPIO.output(mfc1_output_to_chamber_valve, GPIO.HIGH) # Open solenoid valve controlling flow from MFC into chamber
        print(" mfc1_output_to_chamber_valve on")
        GPIO.output(mfc1_venting_valve, GPIO.LOW) # Close solenoid valve venting flow from MFC to atmosphere
        print(" mfc1_venting_valve off")
        GPIO.output(mfc2_output_to_chamber_valve, GPIO.HIGH) # Open solenoid valve controlling flow from MFC into chamber
        print(" mfc2_output_to_chamber_valve on")
        GPIO.output(mfc2_venting_valve, GPIO.LOW) # Close solenoid valve venting flow from MFC to atmosphere
        print(" mfc2_venting_valve off")

        start_time = time.time()
        if methane_injection_time > ethane_injection_time:
            time.sleep( ethane_injection_time )

            GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW) # Close solenoid valve controlling flow from MFC into chamber
            print(" mfc2_output_to_chamber_valve off")

            time.sleep( methane_injection_time - ethane_injection_time )

            GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW) # Close solenoid valve controlling flow from MFC into chamber
            print(" mfc1_output_to_chamber_valve off")


        elif ethane_injection_time > methane_injection_time:
            time.sleep( methane_injection_time )

            GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW) # Close solenoid valve controlling flow from MFC into chamber
            print(" mfc1_output_to_chamber_valve off")

            time.sleep( ethane_injection_time - methane_injection_time )

            GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW) # Close solenoid valve controlling flow from MFC into chamber
            print(" mfc2_output_to_chamber_valve off")


        elif methane_injection_time == ethane_injection_time:
            time.sleep( methane_injection_time )

            GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW) # Close solenoid valve controlling flow from MFC into chamber
            print(" mfc1_output_to_chamber_valve off")

            GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW) # Close solenoid valve controlling flow from MFC into chamber
            print(" mfc2_output_to_chamber_valve off")

        else:
            print("WAT")
            #break

    except: # This is what happens if any errors occur:
        print("Something's wrong!")


def pre_inject_methane():
    print('pre-injecting methane')
    # The "try" and "except" statements dictate what the program does if an error occurs
    try:
        GPIO.output(mfc1_venting_valve, GPIO.HIGH)

        time.sleep(5)

        GPIO.output(mfc1_output_to_chamber_valve, GPIO.HIGH)
#       GPIO.output(mfc1_venting_valve, GPIO.HIGH)

        time.sleep(5)
        
#       GPIO.output(mfc1_output_to_chamber_valve, GPIO.HIGH)
#       
#       time.sleep(15)
        
        GPIO.output(mfc1_venting_valve, GPIO.LOW)
        GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
        
    except: # This is what happens if any errors occur:
        print  ("Something's wrong!")
        

def pre_inject_ethane():
    print('pre-injecting ethane')
    # The "try" and "except" statements dictate what the program does if an error occurs
    try:
        GPIO.output(mfc2_venting_valve, GPIO.HIGH)
        GPIO.output(mfc1_venting_valve, GPIO.HIGH)

        time.sleep(5)

        GPIO.output(mfc2_output_to_chamber_valve, GPIO.HIGH)
        GPIO.output(mfc1_output_to_chamber_valve, GPIO.HIGH)
#       GPIO.output(mfc2_venting_valve, GPIO.HIGH)

        time.sleep(5)
        
#       GPIO.output(mfc2_output_to_chamber_valve, GPIO.HIGH)
#       
#       time.sleep(10)
        
        GPIO.output(mfc2_venting_valve, GPIO.LOW)
        GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
        GPIO.output(mfc1_venting_valve, GPIO.LOW)
        GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
        
    except: # This is what happens if any errors occur:
            print("Something's wrong!")


def pre_inject_methane_and_ethane():
            print('pre-injecting methane and ethane')
            # The "try" and "except" statements dictate what the program does if an error occurs
            try:
                    GPIO.output(mfc1_venting_valve, GPIO.HIGH)
                    GPIO.output(mfc2_venting_valve, GPIO.HIGH)

                    time.sleep(5)

                    GPIO.output(mfc1_output_to_chamber_valve, GPIO.HIGH)
                    GPIO.output(mfc2_output_to_chamber_valve, GPIO.HIGH)
#                    GPIO.output(mfc1_venting_valve, GPIO.HIGH)
#                    GPIO.output(mfc2_venting_valve, GPIO.HIGH)

                    time.sleep(5)
                    
#                    GPIO.output(mfc1_output_to_chamber_valve, GPIO.HIGH)
#                    GPIO.output(mfc2_output_to_chamber_valve, GPIO.HIGH)
#                    
#                    time.sleep(30)
                    
                    GPIO.output(mfc1_venting_valve, GPIO.LOW)
                    GPIO.output(mfc2_venting_valve, GPIO.LOW)
                    GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
                    GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
                    
            except: # This is what happens if any errors occur:
                    print  ("Something's wrong!")
        

def purgeChamber():
    print("Purging chamber")
    # Flush chamber with compressed air
    try:
        # Initial state for outputs:

        GPIO.output(compressed_air_valve, GPIO.LOW)
        GPIO.output(chamber_venting_valve, GPIO.LOW)
        GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
        GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
        GPIO.output(mfc1_venting_valve, GPIO.LOW)
        GPIO.output(mfc2_venting_valve, GPIO.LOW)

        GPIO.output(chamber_venting_valve, GPIO.HIGH) # Open solenoid valve for compressed air venting
        time.sleep(0.5)
        GPIO.output(compressed_air_valve, GPIO.HIGH) # Open solenoid valve for compressed air from compressor

        time.sleep(compressed_air_flush_time) # Wait for allowed sensing chamber flush time

        GPIO.output(compressed_air_valve, GPIO.LOW) # Close solenoid valve for compressed air from compressor
        time.sleep(1)
        # time.sleep(switching_time) # Allow flow/pressure to stabilize for duration of switching_time
        GPIO.output(chamber_venting_valve, GPIO.LOW) # Close solenoid valve for compressed air venting

    except: # This is what happens if any errors occur:
        print("Something's wrong!")


def createFolders(year, month, day):
    ##  Get the path for the folders by year, month and day
    year_path = '/home/pi/Desktop/Hamed_results/' + str(year)
    year_folder = Path(year_path)
    month_path = '/home/pi/Desktop/Hamed_results/' + str(year) + '/' +str(month)
    month_folder = Path(month_path)
    day_path = '/home/pi/Desktop/Hamed_results/' + str(year) + '/' +str(month) + '/' + str(day)
    day_folder = Path(day_path)
    ##  Start creating the folders, when the var complete == True, all the folders have been created
    complete = False
    while complete == False:
        if year_folder.is_dir():
            if month_folder.is_dir():
                if day_folder.is_dir():
                    print ("Today's folder is ready")
                    complete = True
                else:
                    os.makedirs(day_path)
                    print ("Creating today's folder")
                    complete = True       
            else:
                os.makedirs(month_path)
        else:
            os.makedirs(year_path)

    ## This function gets the current time for the time stamp of the txt file and for the folder location

#------------------------Main operation-------------------------------#

##
pre_inject_ethane()
try:
    
    for i in range(numtests):
            
        
        # if ( (methaneConcList[i] > 1100) or (ethaneConcList[i] > 1100) ):
        #     print("Warning! Dangerous levels of combustible gases commanded (>1100 ppm). Exiting program...")
        #     break

        # Do pre-injections
        if p == True:
                    GPIO.output(chamber_venting_valve, GPIO.HIGH)
    #
#                    if ethaneConcList[i] != 0 and methaneConcList[i] != 0:
                    pre_inject_methane_and_ethane()
#                    elif methaneConcList[i] != 0:
#                        pre_inject_methane()
#                    elif ethaneConcList[i] != 0:
#                    pre_inject_ethane()

                    GPIO.output(chamber_venting_valve, GPIO.LOW)

                    purgeChamber()

                    # Do injections
                    if ethaneConcList[i] != 0 and methaneConcList[i] != 0:
                            inject_methane_and_ethane( methaneConcList[i], ethaneConcList[i] )
                    elif methaneConcList[i] != 0:
                            inject_methane( methaneConcList[i] )
                    elif ethaneConcList[i] != 0:
                            inject_ethane( ethaneConcList[i] )
                            
                    GPIO.output(mfc2_venting_valve, GPIO.HIGH)

            
##      This block of code will display the time value every 10 seconds during the diffusion period
        start_time = time.time()
        printing_time_index = 0

##  while loop will run for the duration of the diffusion_time
        while(time.time() < (start_time + diffusion_time) ):
            if(time.time() > (start_time + (printing_time * printing_time_index))):
                printing_time_index += 1 # increment printing_time_index to set time for next print statement
##              if printing_time_index is a multiple of 10, print diffusion timer
                if(((printing_time_index - 1) % 10) == 0):
                    print("Diffusion timer: " + str(float(time.time() - start_time)))

        print('venting chamber before exposure')
        GPIO.output(chamber_venting_valve, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(chamber_venting_valve, GPIO.LOW)
            
#       dataVector1, timeVector = exposeAndCollectData()
#       combinedVector = np.column_stack((timeVector, dataVector1))

  
  
        dataVector1, dataVector2, dataVector3, timeVector = exposeAndCollectData()
        combinedVector = np.column_stack((timeVector, dataVector1, dataVector2, dataVector3))
        # header = [0,temperature, humidity]
        # combinedVector = np.vstack((header, combinedVector))
            
        current_time = datetime.datetime.now()
        year = current_time.year
        month = current_time.month
        day = current_time.day
        createFolders(year, month, day)
        hour = current_time.hour
        minute = current_time.minute
        fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + ':' + 'Methane:' + str(methaneConcList[i]) + '-' + 'Ethane:' + str(ethaneConcList[i]) + '_N35.csv'
        np.savetxt(r'/home/pi/Desktop/Hamed_results/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(fileName), combinedVector, fmt = '%.10f', delimiter = ',')
##        np.savetxt(r'/home/pi/Documents/HETEK_Automation_System_Verification_Results/July_10_Methane'+ str(methaneConcList[i]) + '_' + 'Ethane' + str(ethaneConcList[i]) + '_' + str(data_date_and_time) + '.csv', combinedVector, fmt = '%.10f', delimiter = ',')
##
#except Exception as e:
#    GPIO.output(compressed_air_valve, GPIO.LOW)
#    GPIO.output(chamber_venting_valve, GPIO.LOW)
#    GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
#    GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
#    GPIO.output(mfc1_venting_valve, GPIO.LOW)
#    GPIO.output(mfc2_venting_valve, GPIO.LOW)
#    print("Executed except block")
#    print(e)
        
finally:
    GPIO.output(compressed_air_valve, GPIO.LOW)
    GPIO.output(chamber_venting_valve, GPIO.LOW)
    GPIO.output(mfc1_output_to_chamber_valve, GPIO.LOW)
    GPIO.output(mfc2_output_to_chamber_valve, GPIO.LOW)
    GPIO.output(mfc1_venting_valve, GPIO.LOW)
    GPIO.output(mfc2_venting_valve, GPIO.LOW)
    print("Executed finally block")

    GPIO.cleanup()
    #------------------------End of Main-------------------------------#
