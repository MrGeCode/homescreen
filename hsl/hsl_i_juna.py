import requests
import json
import time

# Define the GraphQL query as a string
query = '''
{
  stations(name: "pohjois") {
    gtfsId
    name
    lat
    lon
    stops {
      gtfsId
      name
      code
      platformCode
    }
  }

  stop(id: "HSL:1294502") {
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

stop(id: "HSL:1294502") {
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

# Send the GraphQL query to the server
response = requests.post(url, json={'query': query})

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
print("Saapuvat junat", stop_data['name'])

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
    print(shortname, eta, "min",headsign)