import requests
import json

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
}
'''

# Define the GraphQL server endpoint URL
url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'

# Send the GraphQL query to the server
response = requests.post(url, json={'query': query})

# Print the response content in a readable format
print(json.dumps(response.json(), indent=2))

