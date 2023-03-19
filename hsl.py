from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.digitransit.fi/timetables/v1/hsl")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    {
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
"""
)

# Execute the query on the transport
result = client.execute(query)
print(result)

