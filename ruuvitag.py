import logging
import os
from datetime import datetime, timedelta
import shutil
import glob
from ruuvitag_sensor.ruuvi import RuuviTagSensor


log_file = '/home/nikopelkonen/workspace/homescreen/data.log'
backup_dir = '/home/nikopelkonen/workspace/homescreen/backup/'

backup_file = backup_dir + 'data_' + datetime.now().strftime('%Y-%m-%d') + '.log'
if not os.path.exists(backup_file):
    shutil.copy(log_file, backup_file)

# Check if the log file is empty or smaller than a threshold size
threshold_size = 1048576  # 1 MB
if os.path.getsize(log_file) < threshold_size:
    # Look for the latest backup file
    backup_files = glob.glob(backup_dir + 'data_*.log')
    latest_backup = max(backup_files, key=os.path.getctime)
    # Check if the latest backup file is larger than the log file
    if os.path.getsize(latest_backup) > os.path.getsize(log_file):
        # Copy the latest backup file to the log file location
        shutil.copy(latest_backup, log_file)

max_backup_age = 3

backup_files = glob.glob(backup_dir + 'data_*.log')
for backup_file in backup_files:
    backup_time = datetime.fromtimestamp(os.path.getctime(backup_file))
    if (datetime.now() - backup_time).days > max_backup_age:
        os.remove(backup_file)


logging.basicConfig(filename='/home/nikopelkonen/workspace/homescreen/data.log', level=logging.INFO)


data_interval = timedelta(minutes=1)
last_saved = {}

def delete_old_logs():
    # Delete data older than one year, except one data point every 15 minutes
    now = datetime.now()
    start_time = now - timedelta(days=365)
    data_to_keep = {}
    with open('/home/nikopelkonen/workspace/homescreen/data.log', 'r') as f:
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
    with open('/home/nikopelkonen/workspace/homescreen/data.log', 'w') as f:
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
