import requests

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
    }
  }  
}
'''

# Define the GraphQL server endpoint URL
url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'

# Send the GraphQL query to the server
response = requests.post(url, json={'query': query})

# Print the response content
print(response.content)

