#!/usr/bin/python3

import requests
import time
import math
import statistics
import weather_math

# create a string to hold the first part of the URL
WUurl = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"
WU_station_id = "KWIMADIS195"
WU_station_pwd = "admqi1gt"
WUcreds = "ID=" + WU_station_id + "&PASSWORD="+ WU_station_pwd
date_str = "&dateutc=now"
action_str = "&action=updateraw"

def upload_weather_data(humidity, ambient_temp, pressure, ground_temp, wind_speed, wind_gust, wind_average, rainfall, daily_rainfall, dew_point):

    ambient_temp_str = "{0:.2f}".format(weather_math.degc_to_degf(ambient_temp))
    ground_temp_str = "{0:.2f}".format(weather_math.degc_to_degf(ground_temp))
    humidity_str = "{0:.2f}".format(humidity)
    pressure_str = "{0:.2f}".format(weather_math.hpa_to_inches(pressure))
    wind_speed_mph_str = "{0:.2f}".format(weather_math.kmh_to_mph(wind_speed))
    wind_gust_mph_str = "{0:.2f}".format(weather_math.kmh_to_mph(wind_gust))
    wind_average_str = str(wind_average)
    rainfall_in_str = "{0:.2f}".format(weather_math.mm_to_inches(rainfall))
    daily_rainfall_in_str = "{0:.2f}".format(weather_math.mm_to_inches(daily_rainfall))
    dew_point_str = "{0:.2f}".format(weather_math.degc_to_degf(dew_point))

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
        "&dailyrainin=" + daily_rainfall_in_str +
        "&soiltempf=" + ground_temp_str +
        "&winddir=" + wind_average_str +
        "&dewptf=" + dew_point_str +
        action_str)

    print(
        WUurl +
        WUcreds +
        date_str +
        "&humidity=" + humidity_str +
        "&baromin=" + pressure_str +
        "&windspeedmph=" + wind_speed_mph_str +
        "&windgustmph=" + wind_gust_mph_str +
        "&tempf=" + ambient_temp_str +
        "&rainin=" + rainfall_in_str +
        "&dailyrainin=" + daily_rainfall_in_str +
        "&soiltempf=" + ground_temp_str +
        "&winddir=" + wind_average_str +
        "&dewptf=" + dew_point_str +
        action_str)
    print("Received " + str(r.status_code) + " " + str(r.text))
