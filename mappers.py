#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split(',')

    # Check if the line has at least 21 fields (columns)
    if len(fields) >= 21:
        date = fields[1]  # YearMonthDay
        wind_speed = fields[12]  # Wind Speed (kt)
        relative_humidity = fields[11]  # % Relative Humidity
        dry_bulb_temp = fields[8]  # Dry Bulb Temp
        dew_point_temp = fields[9]  # Dew Point Temp

        # Emit the date as the key and the required fields as the value
        if wind_speed and relative_humidity and dry_bulb_temp and dew_point_temp:
            print(f'{date}\t{wind_speed}\t{relative_humidity}\t{dry_bulb_temp}\t{dew_point_temp}')