import numpy as np
import logging
import atexit
import pyvisa as visa
import time
import threading

from Instruments.Source_Measure_Unit import Keysight_Source_Measure_Unit_B2902B

samples_per_measure = 20

# check the devices found 
if False:
    rm = visa.ResourceManager()
    resources = rm.list_resources()
    print(resources)


# set the voltage range (initial_point, final_point, step_size) all values in [Volt]
volt_sweep =  list(np.arange(0.05,0.21,0.002)) 

source_meter = Keysight_Source_Measure_Unit_B2902B(address='USB0::0x2A8D::0xB101::MY61391487::INSTR')
source_meter.initialize()
source_meter.configure_channel('1','voltage','1','1e-3')
source_meter.activate_output('1')
source_meter.configure_channel('2','current','1e-6','10')
source_meter.activate_output('2')
print(f"Reading: {source_meter.acquire_data('1','current')}")

#keystroke=input('Press a key \n')

file_name = "acquired_data.txt"
with open(file_name, 'w') as file:
    file.write('Sourced voltage, Measured Current\n')
    for i in volt_sweep:
        source_meter.deactivate_output('1')
        source_meter.configure_channel(f"1','voltage','{i}','1e-3")
        source_meter.activate_output('1')
        for j in range(samples_per_measure):
            file.write(f"{i}, {source_meter.acquire_data('1','current')}")
            time.sleep(0.1)  # not really needed, added for precaution

print("Done")


        
