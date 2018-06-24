#!/usr/bin/python3

import requests
from gpiozero import Button
import time
import math
import wind_direction_byo
import statistics
import bme280
import smbus2
from w1thermsensor import W1ThermSensor

# create a string to hold the first part of the URL
WUurl = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"
WU_station_id = "KWIMADIS195"
WU_station_pwd = "admqi1gt"
WUcreds = "ID=" + WU_station_id + "&PASSWORD="+ WU_station_pwd
date_str = "&dateutc=now"
action_str = "&action=updateraw"

# bme280 sensor
bme280_port = 1
bme280_address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bme280_bus = smbus2.SMBus(bme280_port)

bme280.load_calibration_params(bme280_bus,bme280_address)

def bme280_read_humidity():
    global bme280_address
    global bme280_bus
    bme280_data = bme280.sample(bme280_bus,bme280_address)
    humidity  = bme280_data.humidity
    return humidity

def bme280_read_pressure():
    global bme280_address
    global bme280_bus
    bme280_data = bme280.sample(bme280_bus,bme280_address)
    pressure  = bme280_data.pressure
    return pressure

def bme280_read_ambient_temperature():
    global bme280_address
    global bme280_bus
    bme280_data = bme280.sample(bme280_bus,bme280_address)
    ambient_temperature = bme280_data.temperature
    return ambient_temperature

# ground temp probe
def ds18b20_ground_temp():
    sensor = W1ThermSensor()
    temperature_in_celsius = sensor.get_temperature()
    return temperature_in_celsius


# conversion functions
def hpa_to_inches(pressure_in_hpa):
    pressure_in_inches_of_m = pressure_in_hpa * 0.02953
    return pressure_in_inches_of_m

def mm_to_inches(rainfall_in_mm):
    rainfall_in_inches = rainfall_in_mm * 0.0393701
    return rainfall_in_inches

def degc_to_degf(temperature_in_c):
    temperature_in_f = (temperature_in_c * (9/5.0)) + 32
    return temperature_in_f

def kmh_to_mph(speed_in_kmh):
    speed_in_mph = speed_in_kmh * 0.621371
    return speed_in_mph


humidity = bme280_read_humidity()
ambient_temp = bme280_read_ambient_temperature()
pressure = bme280_read_pressure()
ground_temp = ds18b20_ground_temp()
wind_speed = 5.6129
wind_gust = 12.9030
wind_average = 180
rainfall = 1.270

ambient_temp_str = "{0:.2f}".format(degc_to_degf(ambient_temp))
ground_temp_str = "{0:.2f}".format(degc_to_degf(ground_temp))
humidity_str = "{0:.2f}".format(humidity)
pressure_str = "{0:.2f}".format(hpa_to_inches(pressure))
wind_speed_mph_str = "{0:.2f}".format(kmh_to_mph(wind_speed))
wind_gust_mph_str = "{0:.2f}".format(kmh_to_mph(wind_gust))
wind_average_str = str(wind_average)
rainfall_in_str = "{0:.2f}".format(mm_to_inches(rainfall))

r= requests.get(
    WUurl +
    WUcreds +
    date_str +
    "&humidity=" + humidity_str +
    "&baromin=" + pressure_str +
    "&windspeedmph=" + wind_speed_mph_str +
    "&windgustmph=" + wind_gust_mph_str +
    "&tempf=" + ambient_temp_str +
    "&rainin=" + rainfall_in_str +
    "&soiltempf=" + ground_temp_str +
    "&winddir=" + wind_average_str +
    action_str)

print("Received " + str(r.status_code) + " " + str(r.text))
