import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')

# Function to get stoptimes for a stop ID
def get_stoptimes(stop_id):
    query = '''
    {{
        stop(id: "{stop_id}") {{
            name
            stoptimesWithoutPatterns {{
                scheduledArrival
                realtimeArrival
                arrivalDelay
                scheduledDeparture
                realtimeDeparture
                departureDelay
                realtime
                realtimeState
                serviceDay
                headsign
                trip {{
                    routeShortName
                }}
            }}
        }}
    }}
    '''.format(stop_id=stop_id)

    url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'
    headers = {'digitransit-subscription-key': api_key}
    response = requests.post(url, json={'query': query}, headers=headers)
    stop_data = response.json()['data']['stop']
    stoptimes = stop_data['stoptimesWithoutPatterns']

    headsign_to_shortname = {}
    for stoptime in stoptimes:
        headsign = stoptime['headsign']
        shortname = stoptime['trip']['routeShortName']
        headsign_to_shortname[headsign] = shortname

    output = []
    output.append("Saapuvat junat/bussit " + stop_data['name'])

    for i in range(min(len(stoptimes), 5)):
        stoptime = stoptimes[i]
        headsign = stoptime['headsign']
        scheduled_arrival = stoptime['scheduledArrival']
        realtime_arrival = stoptime['realtimeArrival']
        delay = stoptime['arrivalDelay']
        service_day = stoptime['serviceDay']
        current_time = time.time()
        arrival_time = service_day + realtime_arrival
        eta = int((arrival_time - current_time) / 60)
        shortname = headsign_to_shortname[headsign]
        output.append("{:<5} {:<5} min {}".format(shortname, str(eta) + " ", headsign))

    return output

# Get stoptimes for both stops and update the JSON file every minute
while True:
    output1 = get_stoptimes("HSL:1294502")
    output2 = get_stoptimes("HSL:1293133")

    # Combine the outputs into a dictionary with separate lists
    combined_output = {"stop1": output1, "stop2": output2}

    # Write the combined_output to a JSON file in /var/www/html/ folder
    with open('/var/www/html/hsl.json', 'w') as f:
        json.dump(combined_output, f, indent=4)

    # Wait for 15 seconds before updating again
    time.sleep(15)
