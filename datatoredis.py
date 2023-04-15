import json
import redis
import re

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Create Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Read data.log file
with open('data.log', 'r') as file:
    log_lines = file.readlines()

# Regular expression pattern for MAC address and data
pattern = re.compile(r'MAC ([A-F0-9:]+) - Data ({.+})')

for line in log_lines:
    match = pattern.search(line)

    if match:
        mac_address = match.group(1)
        data = json.loads(match.group(2))

        # Add the timestamp to the data
        timestamp = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}', line).group()
        data['timestamp'] = timestamp

        # Save the data to Redis
        redis_client.rpush(f'{mac_address}:data', json.dumps(data))
