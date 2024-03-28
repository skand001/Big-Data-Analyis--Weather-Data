#!/usr/bin/env python
import sys
from math import sqrt
import logging

logging.basicConfig(filename='processing_errors.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)  # Prevent division by zero

def variance(numbers, mean_val):
    return sum((x - mean_val) ** 2 for x in numbers) / max(len(numbers), 1)  # Prevent division by zero

def pearson_correlation(x, y):
    n = len(x)
    if n == 0: return 0  # Ensure not dividing by zero
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(x_i ** 2 for x_i in x)
    sum_y2 = sum(y_i ** 2 for y_i in y)
    sum_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
    numerator = n * sum_xy - sum_x * sum_y
    denominator = sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
    return numerator / denominator if denominator != 0 else 0

current_date = None
wind_speeds = []
relative_humidities = []
dry_bulb_temps = []
dew_point_temps = []

for line in sys.stdin:
    line = line.strip()
    date, wind_speed, relative_humidity, dry_bulb_temp, dew_point_temp = line.split('\t')

    # No need to re-convert after this block; error handling is now adequate.
    try:
        wind_speed = float(wind_speed)
    except ValueError:
        logging.info(f'Non-convertible wind_speed on {date}: {wind_speed}')
        wind_speed = 0.0  # Default or alternative handling

    try:
        relative_humidity = float(relative_humidity)
    except ValueError:
        logging.info(f'Non-convertible relative_humidity on {date}: {relative_humidity}')
        relative_humidity = 0.0  # Default or alternative handling

    try:
        dry_bulb_temp = float(dry_bulb_temp)
    except ValueError:
        logging.info(f'Non-convertible dry_bulb_temp on {date}: {dry_bulb_temp}')
        dry_bulb_temp = 0.0  # Default or alternative handling

    try:
        dew_point_temp = float(dew_point_temp)
    except ValueError:
        logging.info(f'Non-convertible dew_point_temp on {date}: {dew_point_temp}')
        dew_point_temp = 0.0  # Default or alternative handling
    
    if current_date == date:
        wind_speeds.append(wind_speed)
        relative_humidities.append(relative_humidity)
        dry_bulb_temps.append(dry_bulb_temp)
        dew_point_temps.append(dew_point_temp)
    else:
        if current_date:
            max_wind_speed = max(wind_speeds)
            min_wind_speed = min(wind_speeds)
            min_relative_humidity = min(relative_humidities)
            dew_point_mean = mean(dew_point_temps)
            dew_point_var = variance(dew_point_temps, dew_point_mean)
            corr_rh_ws = pearson_correlation(relative_humidities, wind_speeds)
            corr_rh_dbt = pearson_correlation(relative_humidities, dry_bulb_temps)
            corr_ws_dbt = pearson_correlation(wind_speeds, dry_bulb_temps)

            print(f'{current_date}\t{max_wind_speed - min_wind_speed}\t{min_relative_humidity}\t{dew_point_mean}\t{dew_point_var}\t{corr_rh_ws}\t{corr_rh_dbt}\t{corr_ws_dbt}')

        current_date = date
        wind_speeds = [wind_speed]
        relative_humidities = [relative_humidity]
        dry_bulb_temps = [dry_bulb_temp]
        dew_point_temps = [dew_point_temp]

if current_date:
    max_wind_speed = max(wind_speeds)
    min_wind_speed = min(wind_speeds)
    min_relative_humidity = min(relative_humidities)
    dew_point_mean = mean(dew_point_temps)
    dew_point_var = variance(dew_point_temps, dew_point_mean)
    corr_rh_ws = pearson_correlation(relative_humidities, wind_speeds)
    corr_rh_dbt = pearson_correlation(relative_humidities, dry_bulb_temps)
    corr_ws_dbt = pearson_correlation(wind_speeds, dry_bulb_temps)

    print(f'{current_date}\t{max_wind_speed - min_wind_speed}\t{min_relative_humidity}\t{dew_point_mean}\t{dew_point_var}\t{corr_rh_ws}\t{corr_rh_dbt}\t{corr_ws_dbt}')