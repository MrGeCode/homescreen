import re
import json
import time
from datetime import datetime, timedelta, time as datetime_time

print("Starting printtemptojson.py...")

# Provide the correct file path
log_file_path = "/home/nikopelkonen/workspace/homescreen/data.log"

# Set the output file path
output_file_path = "/var/www/html/temperature.json"

while True:
    # Initialize variables
    sensors_data = []

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

                    sensor_data = next((sd for sd in sensors_data if sd["id"] == "ulkotila"), None)
                    if not sensor_data:
                        sensor_data = {"id": "ulkotila", "data": []}
                        sensors_data.append(sensor_data)

                    sensor_data["data"].append({"timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"), "temperature": temperature})

    # Save the temperature data to a JSON file
    sensors_json_data = []
    for sensor_data in sensors_data:
        data = sensor_data["data"]
        latest_temperature = data[-1]["temperature"]
        highest_temperature = max([d["temperature"] for d in data])
        lowest_temperature = min([d["temperature"] for d in data])
        latest_timestamp = data[-1]["timestamp"]
        sensors_json_data.append({"id": sensor_data["id"], "timestamp": latest_timestamp, "latest_temperature": latest_temperature, "highest_temperature": highest_temperature, "lowest_temperature": lowest_temperature})

    sensors_json = {"sensors": sensors_json_data}

    with open(output_file_path, "w") as json_file:
        json.dump(sensors_json, json_file)

    # Wait for a minute before updating the file again
    time.sleep(60)
