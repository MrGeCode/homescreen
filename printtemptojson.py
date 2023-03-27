import re
from datetime import datetime, time, timedelta
import json
import time as t

# Initialize variables
latest_temperature = None
highest_temperature = None
lowest_temperature = None
latest_timestamp = None

html_file_path = "/var/www/html/temperature.json"
log_file_path = "/home/nikopelkonen/workspace/homescreen/data.log"

while True:
    # Get current time
    now = datetime.now().time()
    is_night = (now >= time(23, 0) or now < time(6, 0))

    # Determine refresh interval based on time of day
    if is_night:
        refresh_interval = timedelta(minutes=10)
    else:
        refresh_interval = timedelta(minutes=2)

    # Initialize data dictionary
    data_dict = {}

    # Open the log file and read the lines
    with open(log_file_path, "r") as log_file:
        for line in log_file.readlines():
            # Check if the line starts with INFO:root and contains the desired MAC address
            if line.startswith("INFO:root") and "MAC F3:DB:14:E5:BD:FB" in line:

                # Extract the timestamp and data dictionary using regex
                timestamp_str, data_str = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}) - MAC F3:DB:14:E5:BD:FB - Data (.+)$", line).groups()

                # Convert the timestamp to a datetime object
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

                # Check if the timestamp is within the refresh interval
                if (datetime.now() - timestamp) <= refresh_interval:
                    # Parse the data dictionary
                    data = eval(data_str)
                    temperature = data["temperature"]

                    # Update the latest, highest, and lowest temperatures
                    if latest_timestamp is None or timestamp > latest_timestamp:
                        latest_temperature = temperature
                        latest_timestamp = timestamp

                    if highest_temperature is None or temperature > highest_temperature:
                        highest_temperature = temperature

                    if lowest_temperature is None or temperature < lowest_temperature:
                        lowest_temperature = temperature

        # Populate data dictionary
        data_dict["latest"] = latest_temperature
        data_dict["highest"] = highest_temperature
        data_dict["lowest"] = lowest_temperature

    # Write data dictionary to JSON file
    with open(html_file_path, "w") as html_file:
        json.dump(data_dict, html_file)

    # Sleep until next refresh interval
    t.sleep(refresh_interval.seconds)
