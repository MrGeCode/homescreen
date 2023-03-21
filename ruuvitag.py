import logging
import os
from datetime import datetime, timedelta
from ruuvitag_sensor.ruuvi import RuuviTagSensor

logging.basicConfig(filename='data.log', level=logging.INFO)

data_interval = timedelta(minutes=1)
last_saved = {}

def delete_old_logs():
    # Delete data older than one year, except one data point every 15 minutes
    now = datetime.now()
    start_time = now - timedelta(days=365)
    data_to_keep = {}
    with open('data.log', 'r') as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) != 3:
            continue
        try:
            log_time = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S.%f')
            mac = parts[1].split(' ')[-1]
        except ValueError:
            continue
        if log_time >= start_time:
            data_to_keep[mac] = log_time
        elif log_time.minute % 15 == 0:
            if mac not in data_to_keep or log_time > data_to_keep[mac]:
                data_to_keep[mac] = log_time
    with open('data.log', 'w') as f:
        for line in lines:
            parts = line.strip().split(' - ')
            if len(parts) != 3:
                f.write(line)
                continue
            try:
                log_time = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S.%f')
                mac = parts[1].split(' ')[-1]
            except ValueError:
                f.write(line)
                continue
            if mac in data_to_keep and log_time == data_to_keep[mac]:
                f.write(line)

def handle_data(found_data):
    mac = found_data[0]
    data = found_data[1]
    now = datetime.now()

    # Save data point every minute
    if mac not in last_saved or now - last_saved[mac] >= data_interval:
        logging.info(f"{now} - MAC {mac} - Data {data}")
        last_saved[mac] = now

    # Delete old log data and keep one data point every 15 minutes after one year
    if now.date() != datetime(2024, 3, 21).date():
        delete_old_logs()

if __name__ == "__main__":
    RuuviTagSensor.get_data(handle_data)
