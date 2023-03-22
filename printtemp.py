import datetime
import ast

filename = '/home/nikopelkonen/workspace/homescreen/data.log'

with open(filename, 'r') as file:
    lines = file.readlines()
    print(f"Number of lines read from file: {len(lines)}")
    
    latest_temperatures = {}
    for line in lines:
        if line.startswith('INFO:root:'):
            parts = line.split()
            mac_address = parts[3]
            print(f"MAC address found in line: {mac_address}")
            if mac_address == 'F3:DB:14:E5:BD:FB':
                timestamp = datetime.datetime.strptime(parts[1] + ' ' + parts[2], '%Y-%m-%d %H:%M:%S.%f')
                data = ast.literal_eval(' '.join(parts[5:]))
                print(f"Data dictionary for line: {data}")
                if 'temperature' in data:
                    temperature = data['temperature']
                    latest_temperatures[timestamp] = temperature
                    print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Temperature: {temperature}       C")

    if latest_temperatures:
        latest_time = max(latest_temperatures.keys())
        lowest_temp = min(latest_temperatures.values())
        highest_temp = max(latest_temperatures.values())
        current_temp = latest_temperatures[latest_time]

        print(f"\nCurrent temperature: {current_temp}       C")
        print(f"Highest temperature since midnight: {highest_temp}       C")
        print(f"Lowest temperature since midnight: {lowest_temp}       C")
    else:
        print("No temperature readings found for MAC address F3:DB:14:E5:BD:FB")
