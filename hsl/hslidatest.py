import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('API_KEY')

# Define the GraphQL query as a string
query = '''
{
  stop(id: "HSL:1293133") {
    name
      stoptimesWithoutPatterns {
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
      trip {
        routeShortName
      }
    }
 }


stop(id: "HSL:1293133") {
    gtfsId
    name
    lat
    lon
    patterns {
      code
      directionId
      headsign
      route {
        gtfsId
        shortName
        longName
        mode
      }
    }
  }
}
'''

# Define the GraphQL server endpoint URL
url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'

# Get the API key from an environment variable
api_key = os.environ.get('API_KEY')

# Send the GraphQL query to the server with the API key in the headers
response = requests.post(url, json={'query': query}, headers={'digitransit-subscription-key': api_key})

# Extract the stop data from the response
stop_data = response.json()['data']['stop']

# Extract the list of stoptimesWithoutPatterns from the stop data
stoptimes = stop_data['stoptimesWithoutPatterns']

# Create a dictionary to map headsigns to short names
headsign_to_shortname = {}
for stoptime in stoptimes:
    headsign = stoptime['headsign']
    shortname = stoptime['trip']['routeShortName']
    headsign_to_shortname[headsign] = shortname

# Print the name of the stop
print("Saapuvat bussit", stop_data['name'])

# Iterate through the first 5 stoptimes and print their short name, headsign, and ETA in minutes
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
    print("{:<5} {:<5} min {}".format(shortname, str(eta) + " ", headsign))
    # Padding the shortname to a fixed width of 5 characters, and adding a space after the ETA
    # Using the newline character to separate the lines
