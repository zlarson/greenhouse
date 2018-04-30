 
import os
import glob
import time
import peewee
from peewee import *
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

db = MySQLDatabase('Greenhouse', user='greenhouseuser', passwd='', port=3306)

class TemperatureReading(peewee.Model):
    internal_temperature = peewee.DecimalField()
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0

        TemperatureReading.create_table()
        temp = TemperatureReading(internal_temperature=temp_f)
        temp.save()

        return temp_c, temp_f

while True:
        print(read_temp())
        time.sleep(1)
