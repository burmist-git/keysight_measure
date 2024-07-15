# Example usage:
# source_meter = Keysight_Source_Measure_Unit_B2902B(address='USB0::0x2A8D::0xB101::MY61391487::INSTR')
#source_meter.initialize()
#source_meter.configure_channel('1','voltage','1','1e-3')
#source_meter.activate_output('1')
#source_meter.configure_channel('2','current','1e-6','10')
#source_meter.activate_output('2')
#print(f"Reading: {source_meter.acquire_data('1','current')}")

import pyvisa
import socket
import time

class Keysight_Source_Measure_Unit_B2902B:
    def operation_wait(self):
        ready = 0
        while ready == 0 :
            ready = self.instrument.query('*OPC?')
            time.sleep(0.5)

    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(address)
        self.instrument.timeout = 5000  # Timeout in milliseconds
        self._channelON       = [False,False]
    
    def initialize(self):
        self.instrument.write('*RST')  # Reset the instrument
        self.operation_wait()
        self.instrument.write('*CLS')  # Clear the status
        self.operation_wait()
        self.instrument.query('*CAL?')  # Clear the status
        self.operation_wait()

        for i in [1,2]:
            cmd = f"SOUR{i}:VOLT:MODE FIX"
            print(cmd)
            self.instrument.write(f"SOUR{i}:VOLT:MODE FIX")
            # Set the measurement to current
            self.instrument.write(f'SENS1:CURR:PROT 1e-3')
            print(self.query(':SYSTEM:ERROR:ALL?'))
            #keystroke=input('Press a key \n')

            # Set default voltage range
            self.instrument.write(f"SOUR{i}:VOLT:RANG:AUTO 1")
            # Set default current range
            self.instrument.write(f"SENS{i}:CURR:RANG:AUTO 1")
            self.instrument.write(f"SENS{i}:CURR:RANG:AUTO:MODE RES")
        #print(self.instrument.query(":SYST:AZER?"))
        print("Unit initialized and set to Voltage-source / Current-measure.")
    
    def configure_channel(self, channel='1', source='voltage', amplitude='0.001', compliance='0.001'):
        if source == 'voltage':
            mode = 'VOLT'
            limit = 'CURR'
        elif source == 'current':
            mode = 'CURR'
            limit = 'VOLT'
        else: 
            print('ERROR: Selected source invalid')
            return
        self.write(f':SOUR{channel}:FUNC:MODE {mode}')
        self.write(f':SOUR{channel}:{mode} {amplitude}')
        self.write(f':SENS{channel}:{limit}:PROT:POS {compliance}')

    def acquire_data(self, channel='1', measure='voltage'):
        # measure: voltage, current, resistance
        if measure == 'voltage':
            mode = 'VOLT' 
        elif measure == 'current':
            mode = 'CURR'
        elif measure == 'resistance':
            mode = 'RES'
        else:
            print('ERROR: Measure type invalid')
            return
        return self.query(f':MEAS:{mode}? (@{channel})')



    def activate_output(self, channel='1'):
        self.write(f':OUTP{channel} ON')
        
    def deactivate_output(self, channel='1'):
        self.write(f':OUTP{channel} OFF')
        
   
    def close(self):
        self.instrument.close()
        self.rm.close()
        print("Connection to Source Meter closed.")
    def write(self, message: str):

        self.instrument.write(message)

    def query(self, message: str):

        reply = self.instrument.query(message)

        return reply

    def read(self):

        return self.instrument.read()

