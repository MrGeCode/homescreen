import re
import json
import time
from datetime import datetime, timedelta, time as datetime_time

# Initialize variables
latest_temperature = None
highest_temperature = None
lowest_temperature = None
latest_timestamp = None

# Provide the correct file path
log_file_path = "/home/nikopelkonen/workspace/homescreen/data.log"

# Set the output file path
output_file_path = "/var/www/html/temperature.json"

while True:
    today_midnight = datetime.combine(datetime.today(), datetime_time(0, 0))
    tomorrow_midnight = today_midnight + timedelta(days=1)

    # Open the log file and read the lines
    with open(log_file_path, "r") as log_file:
        for line in log_file.readlines():
            if line.startswith("INFO:root") and "MAC F3:DB:14:E5:BD:FB" in line:

                timestamp_str, data_str = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}) - MAC F3:DB:14:E5:BD:FB - Data (.+)$", line).groups()

                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

                if today_midnight <= timestamp < tomorrow_midnight:
                    data = eval(data_str)
                    temperature = data["temperature"]

                    if latest_timestamp is None or timestamp > latest_timestamp:
                        latest_temperature = temperature
                        latest_timestamp = timestamp

                    if highest_temperature is None or temperature > highest_temperature:
                        highest_temperature = temperature

                    if lowest_temperature is None or temperature < lowest_temperature:
                        lowest_temperature = temperature

    # Save the temperature data to a JSON file
    temperature_data = {
        "latest_temperature": latest_temperature,
        "highest_temperature": highest_temperature,
        "lowest_temperature": lowest_temperature
    }

    with open(output_file_path, "w") as json_file:
        json.dump(temperature_data, json_file)

    # Wait for a minute before updating the file again
    time.sleep(60)

