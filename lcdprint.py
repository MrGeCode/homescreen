import re
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from datetime import datetime, time, timedelta
import time

# Initialize variables
latest_temperature = None
highest_temperature = None
lowest_temperature = None
latest_timestamp = None

today_midnight = datetime.combine(datetime.today(), time(0, 0))
tomorrow_midnight = today_midnight + timedelta(days=1)

# Provide the correct file path
log_file_path = "/home/nikopelkonen/workspace/homescreen/data.log"

# Initialize I2C bus and LCD object
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_I2C(i2c, 20, 4)

# Loop indefinitely
while True:
    # Open the log file and read the lines
    with open(log_file_path, "r") as log_file:
        for line in log_file.readlines():
            # Check if the line starts with INFO:root and contains the desired MAC address
            if line.startswith("INFO:root") and "MAC F3:DB:14:E5:BD:FB" in line:

                # Extract the timestamp and data dictionary using regex
                timestamp_str, data_str = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}) - MAC F3:DB:14:E5:BD:FB - Data (.+)$", line).groups()

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

    # Display the latest, highest, and lowest temperatures on the LCD screen
    lcd.clear()
    lcd.message = f"Ulkol\xE4mp\xF6tila: {latest_temperature:.1f}\xDFC\n" \
                  f"\x1E {highest_temperature:.1f}\xDFC   \x1F {lowest_temperature:.1f}\xDFC"

    # Delay for 1 minute before reading the log file and updating the LCD again
    time.sleep(60)
