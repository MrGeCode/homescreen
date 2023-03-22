import re
from datetime import datetime, time, timedelta

# Initialize variables
latest_temperature = None
highest_temperature = None
lowest_temperature = None
latest_timestamp = None

today_midnight = datetime.combine(datetime.today(), time(0, 0))
tomorrow_midnight = today_midnight + timedelta(days=1)

# Provide the correct file path
log_file_path = "/home/nikopelkonen/workspace/homescreen/data.log"

# Open the log file and read the lines
with open(log_file_path, "r") as log_file:
    for line in log_file.readlines():
        # Check if the line starts with INFO:root and contains the desired MAC address
        if line.startswith("INFO:root") and "MAC E1:EE:8A:A0:01:C5" in line:

            # Extract the timestamp and data dictionary using regex
            timestamp_str, data_str = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}) - MAC E1:EE:8A:A0:01:C5 - Data (.+)$", line).groups()

            # Convert the timestamp to a datetime object
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

            # Check if the timestamp is between today midnight and tomorrow midnight
            if today_midnight <= timestamp < tomorrow_midnight:
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

print(f"Sisälämpötila: {latest_temperature}°C")
print(f"'\u2191': {highest_temperature}°C")
print(f"'\u2193': {lowest_temperature}°C")
