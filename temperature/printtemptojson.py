import redis
import json
from datetime import datetime
from time import sleep

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Create Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_data_points(mac_address):
    data_points = redis_client.lrange(mac_address + ':data', 0, -1)
    return [json.loads(data_point.decode()) for data_point in data_points]

def generate_temperature_json(mac_address_to_id):
    temperature_data = []

    for mac_address, location_id in mac_address_to_id.items():
        data_points = get_data_points(mac_address)

        if not data_points:
            continue

        # Filter data points to only include those from the current day
        current_day_data_points = [data_point for data_point in data_points if datetime.strptime(data_point['timestamp'], "%Y-%m-%d %H:%M:%S.%f").date() == datetime.today().date()]

        if not current_day_data_points:
            continue

        latest_temperature = current_day_data_points[-1]['temperature']
        highest_temperature = max(data_point['temperature'] for data_point in current_day_data_points)
        lowest_temperature = min(data_point['temperature'] for data_point in current_day_data_points)
        timestamp = current_day_data_points[-1]['timestamp']

        temperature_data.append({
            "id": location_id,
            "timestamp": timestamp,
            "latest_temperature": latest_temperature,
            "highest_temperature": highest_temperature,
            "lowest_temperature": lowest_temperature
        })

    return temperature_data

if __name__ == '__main__':
    # Replace with your actual MAC addresses and location IDs
    mac_address_to_id = {
        'E1:EE:8A:A0:01:C5': 'sisatila',
        'F3:DB:14:E5:BD:FB': 'ulkotila'
    }

    output_file_path = "/var/www/html/temperature.json"

    while True:
        temperature_data = generate_temperature_json(mac_address_to_id)

        with open(output_file_path, 'w') as file:
            json.dump(temperature_data, file, indent=4)

        sleep(15)
