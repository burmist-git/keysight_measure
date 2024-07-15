import pyvisa
import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime

## Set the input parameters for the IV curve
averages = 10
fwd_voltage = -1.2  # Minimum forward bias voltage
min_voltage = 0.0   # Voltage to start coarse scan in reverse bias
inter_voltage = 40.0  # Voltage to start fine scan in forward bias
max_voltage = 41.0  # Voltage to stop the scan

## Define number of data points
data_points = {}
data_points['fwd'] = int((min_voltage - fwd_voltage) * 20 + 1)    # Number of points for forward bias scan
data_points['coarse'] = int((inter_voltage - min_voltage) + 1)     # Number of points for coarse scan
data_points['fine'] = int((max_voltage - inter_voltage) * 2) + 1   # Number of points for fine scan

## Initialize the VISA resource manager and connect to the instrument
rm = pyvisa.ResourceManager()
inst = rm.open_resource('TCPIP0::192.168.0.101')  # Update with the correct VISA address for your Keysight B2902B
inst.write("*RST")  # Reset the instrument

## Source settings
inst.write(":SOUR:FUNC VOLT")      # Set source function to DC voltage
inst.write(":SOUR:VOLT:RANG 100")  # Set source range to 100 V
inst.write(":SOUR:CURR:PROT 0.1")  # Set current protection level to 0.1 A

## Initial measurement range
starting_range = 1e-4  # Adjust according to instrument specifications

## Measurements settings
inst.write(":SENS:FUNC 'CURR:DC'")             # Set measurement function to DC current
inst.write(":SENS:CURR:PROT:LEV 0.1")           # Set current protection level to 0.1 A
inst.write(":SENS:CURR:RANG:AUTO ON")          # Enable auto-ranging for current measurement
inst.write(":SENS:CURR:NPLC 10")               # Set integration time to 10 PLC

## Main measurement loop
loop = 0
run_ = True

while run_:
    print('############################ Measurement number %s ####################################' % loop)

    # Perform autozero and wait for instrument to settle
    inst.write(":SYST:AZER:ONCE")
    sleep(10)  # Adjust sleep time as necessary for stabilization

    # Allocate arrays to store the measurement results
    voltages = {}
    currents = {}

    # Define the voltage steps for measurement (only fine region of IV curve is measured here)
    voltages['fine'] = np.linspace(inter_voltage, max_voltage, num=data_points['fine'])

    # Get the current date and time
    now = datetime.now()
    t = now.strftime("%Y-%m-%d_%H-%M-%S")
    print("Time:", t)

    # Initialize current measurement arrays
    for j in range(100):
        name_ = 'fine_sample_' + str(j)
        currents[name_] = np.zeros_like(voltages['fine'])

    # Set measurement range and turn on source output
    inst.write(":SENS:CURR:RANG %s" % starting_range)
    inst.write(":OUTP ON")

    # Loop over the voltages and perform measurements
    for i, voltage in enumerate(voltages['fine']):
        inst.write(":SOUR:VOLT:LEV %s" % voltage)  # Set the source voltage

        # Perform 100 measurements for each voltage
        for j in range(100):
            inst.write(":READ?")  # Trigger measurement and read current
            current = float(inst.read())
            name_ = 'fine_sample_' + str(j)
            currents[name_][i] = current

            if j == 99:
                print(current)
                print(voltage)

    # Change source level in steps to zero to avoid electrical stress and manage thermal effects
    inst.write(":SOUR:VOLT:LEV 45")
    sleep(1)
    inst.write(":SOUR:VOLT:LEV 34")
    sleep(1)
    inst.write(":SOUR:VOLT:LEV 25")
    sleep(1)
    inst.write(":SOUR:VOLT:LEV 15")
    sleep(1)
    inst.write(":SOUR:VOLT:LEV 5")
    sleep(1)
    inst.write(":OUTP OFF")  # Turn off source output

    # Create a DataFrame to store voltage and current data
    d = {'voltage V': voltages['fine']}
    data1 = pd.DataFrame(data=d)
    for j in range(100):
        name_0 = 'fine_sample_' + str(j)
        name_ = 'Current (S' + str(j) + ', A)'
        data1[name_] = currents[name_0]

    # Save the DataFrame to a CSV file
    folder_name = r'D:\downloaded-files'
    file_name_ = os.path.join(folder_name, '%s-finesample.csv' % now.strftime("%Y-%m-%d_%H-%M"))
    data1.to_csv(file_name_, index=False)

    # 15-minute break between each set of measurements
    sleep(900)
    loop += 1  # Increment loop counter

