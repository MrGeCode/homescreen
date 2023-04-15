import redis
import json
from datetime import datetime, timedelta
from ruuvitag_sensor.ruuvi import RuuviTagSensor

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Create Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Interval to save data to Redis (in seconds)
SAVE_INTERVAL = 60

# Last time data was saved to Redis
last_save_time = datetime.now()

def save_data_to_redis(mac_address, data):
    # Add timestamp to the data
    redis_time = redis_client.time()  # get current server time
    timestamp = datetime.fromtimestamp(redis_time[0] + redis_time[1] / 1000000).strftime("%Y-%m-%d %H:%M:%S.%f")
    data['timestamp'] = timestamp

    # Convert data to JSON string
    data_json = json.dumps(data)

    # Save data to Redis with key as MAC address
    redis_client.rpush(mac_address + ':data', data_json)

def handle_data(found_data):
    global last_save_time  # Import the global variable to update it

    mac_address = found_data[0]
    data = found_data[1]
    # Save data point to dictionary
    ruuvi_data[mac_address] = data

    # Check if it's time to save data to Redis
    if (datetime.now() - last_save_time) >= timedelta(seconds=SAVE_INTERVAL):
        # Save data to Redis for each sensor
        for mac_address, data in ruuvi_data.items():
            save_data_to_redis(mac_address, data)
        # Clear dictionary
        ruuvi_data.clear()
        # Update the last_save_time
        last_save_time = datetime.now()

if __name__ == '__main__':
    # Create dictionary to store RuuviTag data
    ruuvi_data = {}

    # Start listening for RuuviTag data
    RuuviTagSensor.get_data(handle_data)
