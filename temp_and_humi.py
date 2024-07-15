#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
from Instruments.yocto_api import *
from Instruments.yocto_temperature import *
from Instruments.yocto_humidity import *
from datetime import datetime, date
import os.path as path

def die(msg):
    sys.exit(msg + ' (check USB cable)')

def get_temp_and_humi() :
    errmsg = YRefParam()

    # Setup the API to use local USB devices
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        sys.exit("init error" + errmsg.value)

    # retreive any temperature sensor
    sensor_t = YTemperature.FirstTemperature()
    sensor_h = YHumidity.FirstHumidity()
    if sensor_t is None:
        die('No module connected')

    if not (sensor_t.isOnline()):
        die('device not connected')

    col = ['Datetime', 'Temperature', 'Humidity']
    
    if sensor_t.isOnline():
        temp = sensor_t.get_currentValue()
        hum = sensor_h.get_currentValue()
        #print(str(datetime.now())+", Temp:  " + "%2.1f" % sensor_t.get_currentValue() + "°C, Humi: " + "%2.1f" % sensor_h.get_currentValue() + " %")
        return temp, hum
        
    YAPI.FreeAPI()

if __name__ == "__main__":
    temp, hum = get_temp_and_humi()
    print(str(datetime.now())+", Temp:  " + "%2.1f" % temp + "°C, Humi: " + "%2.1f" % hum + " %")
