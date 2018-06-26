#!/usr/bin/python3

from gpiozero import Button
import time
import math
#import bme280_sensor
import wind_direction
import statistics
import database
import decimal
#import ds18b20_therm
import wu_upload

CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
ADJUSTMENT = 1.18
BUCKET_SIZE = 0.2794

interval = 10
radius_cm = 9.0
wind_interval = 5
wind_count = 0
rain_count = 0

store_speeds = []
store_directions = []

def spin():
    global wind_count
    wind_count = wind_count + 1
    #print("spin" + str(wind_count))

def calculate_speed(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    dist_km = (circumference_cm * rotations) / CM_IN_A_KM

    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR

    return km_per_hour * ADJUSTMENT

def reset_wind():
    global wind_count
    wind_count = 0

def bucket_tipped():
    global rain_count
    rain_count = rain_count + 1
    #print (rain_count * BUCKET_SIZE)

def reset_rainfall():
    global rain_count
    rain_count = 0

rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped

wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin
def direction(wind_average):
    direction = "Null"
    if wind_average <= 89.9:
        direction = "North"
    elif wind_average <= 179.9:
        direction = "East"
    elif wind_average <= 269.9:
        direction = "South"
    elif wind_average <= 360.0:
        direction = "West"
    return direction

db = database.weather_database()

while True:
    start_time = time.time()
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction.get_value())

        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    wind_average = wind_direction.get_average(store_directions)
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    rainfall = rain_count * BUCKET_SIZE
    reset_rainfall()
    humidity = 0
    pressure = 0
    ambient_temp = 0
    ground_temp = 0
    #humidity, pressure, ambient_temp = bme280_sensor.read_all()
    print("wind speed: " + str(wind_speed))
    print("wind gust: " + str(wind_gust))
    print("rainfall: " + str(rainfall))
    print("wind direction: " + str(direction(wind_average)))
    #print("humidity: " + str(humidity)),
    #print("pressure: " + str(pressure)),
    #print("ambient_temp: " + str((ambient_temp * (9.0/5.0)) + 32.0 ))
    humidity=0
    pressure=0
    ambient_temp=0
    db.insert(ambient_temp, ground_temp, 0, pressure, humidity, round(wind_average,2), round(wind_speed,2), round(wind_gust,2), round(rainfall,2))
    db.select_rain_last_hour
    wu_upload.upload_weather_data(humidity, ambient_temp, pressure, ground_temp, wind_speed, wind_gust, wind_average, rainfall)
    store_speeds = []
    store_directions = []
