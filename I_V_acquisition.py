import numpy as np
import logging
import atexit
import pyvisa as visa
import time
import threading
from Instruments.Source_Measure_Unit import Keysight_Source_Measure_Unit_B2902B

# USER DEFINED VARIABLES

## Set the input parameters for the IV curve
samples_per_measure = 20  # define the number of acquisition per sweep-point
fwd_voltage = -1.5        # Minimum forward bias voltage
min_voltage = 0.0         # Voltage to start coarse scan in reverse bias
inter_voltage = 30.0      # Voltage to start fine scan in forward bias
max_voltage = 42.0        # Voltage to stop the scan

## Define number of data points
data_points = {}
data_points['fwd'] = 20                                            # Number of points for forward bias scan
data_points['coarse'] = 20                                         # Number of points for coarse scan
data_points['fine'] = int((max_voltage - inter_voltage) * 4) + 1   # Number of points for fine scan
#
volt_sweep = list(np.linspace(fwd_voltage,min_voltage,data_points['fwd']))
volt_sweep.extend(list(np.linspace(min_voltage,inter_voltage,data_points['coarse'])))
volt_sweep.extend(list(np.linspace(inter_voltage,max_voltage,data_points['fine'])))
print(data_points)
print(volt_sweep)
#
#keystroke=input('Press a key \n')

file_name = "acquired_data.txt"

# Code to check the VISA devices that can be reached 
if False:
    rm = visa.ResourceManager()
    resources = rm.list_resources()
    print(resources)
    keystroke=input('Press a key \n')


# instantiate the instrument and intialization with default values
source_meter = Keysight_Source_Measure_Unit_B2902B(address='USB0::0x2A8D::0xB101::MY61391487::0::INSTR')
source_meter.initialize()
#print(source_meter.query(':SYSTEM:ERROR:ALL?'))
#keystroke=input('Press a key \n')

source_meter.configure_channel('1','voltage','1','1e-3')
#print(source_meter.query(':SYSTEM:ERROR:ALL?'))
#keystroke=input('Press a key \n')

source_meter.activate_output('1')
#print(source_meter.query(':SYSTEM:ERROR:ALL?'))
#keystroke=input('Press a key \n')

time.sleep(1)
source_meter.acquire_data('1','voltage')
source_meter.configure_channel('2','voltage','0','20e-3')
#print(source_meter.query(':SYSTEM:ERROR:ALL?'))
#keystroke=input('Press a key \n')

source_meter.activate_output('2')
#print(source_meter.query(':SYSTEM:ERROR:ALL?'))
#keystroke=input('Press a key \n')

# for debugging
#print(f"Reading ch1: {source_meter.acquire_data('1','current')}")
#print(f"Reading ch2: {source_meter.acquire_data('2','current')}")
#print(f'Voltage_sweep: {volt_sweep}')
#keystroke=input('Press a key \n')

# write data to file
with open(file_name, 'a') as file:
    file.write('Sourced_voltage,Channel_Current\n')
    for i in volt_sweep:
        #source_meter.deactivate_output('1')
        #time.sleep(1)
        source_meter.configure_channel('1','voltage',i,'20e-3')
        #source_meter.activate_output('1')
        time.sleep(1)
        source_meter.acquire_data('1','current')
        for j in range(samples_per_measure):
            file.write(f"{i},{source_meter.acquire_data('2','current')}")
            time.sleep(0.1)  # not really needed, added for precaution
source_meter.deactivate_output('1')
source_meter.deactivate_output('2')
source_meter.write(':SYST:BEEP:IMM 1000,1')
time.sleep(2.0)
source_meter.write(':SYST:BEEP:IMM 1000,1')
time.sleep(2.0)
source_meter.write(':SYST:BEEP:IMM 1000,5')

print(source_meter.query(':SYSTEM:ERROR:ALL?'))
print("Done")
