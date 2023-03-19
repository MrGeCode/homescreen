api url `GET https://api.digitransit.fi/timetables/v1/hsl`


https://digitransit.fi/en/developers/apis/1-routing-api/stops/


```
{
  "data": {
    "stops": [
      {
        "gtfsId": "HSL:1293133",
        "name": "Ida Aalbergin tie",
        "code": "H1658",
        "lat": 60.228669,
        "lon": 24.894889
      },
      {
        "gtfsId": "HSL:1293132",
        "name": "Ida Aalbergin tie",
        "code": "H1659",
        "lat": 60.229985,
        "lon": 24.895234
      }
    ]
  }
}
```

Information about HSL:1293133 stop
```
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
response
{
  "data": {
    "stop": {
      "gtfsId": "HSL:1293133",
      "name": "Ida Aalbergin tie",
      "lat": 60.228669,
      "lon": 24.894889,
      "patterns": [
        {
          "code": "HSL:1052:0:01",
          "directionId": 0,
          "headsign": "Otaniemi",
          "route": {
            "gtfsId": "HSL:1052",
            "shortName": "52",
            "longName": "Kuninkaantammi-Kannelmäki-Huopalahti-Munkkivuori-Otaniemi",
            "mode": "BUS"
          }
        },
        {
          "code": "HSL:1031:0:01",
          "directionId": 0,
          "headsign": "Munkkivuori",
          "route": {
            "gtfsId": "HSL:1031",
            "shortName": "31",
            "longName": "Pohjois-Haaga-Munkkivuori",
            "mode": "BUS"
          }
        },
        {
          "code": "HSL:1040:1:01",
          "directionId": 1,
          "headsign": "Elielinaukio",
          "route": {
            "gtfsId": "HSL:1040",
            "shortName": "40",
            "longName": "Elielinaukio-Haaga-Kannelmäki",
            "mode": "BUS"
          }
        },
        {
          "code": "HSL:1032:0:01",
          "directionId": 0,
          "headsign": "Munkkivuori",
          "route": {
            "gtfsId": "HSL:1032",
            "shortName": "32",
            "longName": "Pohjois-Haaga-Munkkivuori",
            "mode": "BUS"
          }
        },
        {
          "code": "HSL:1056:1:01",
          "directionId": 1,
          "headsign": "Kalasatama",
          "route": {
            "gtfsId": "HSL:1056",
            "shortName": "56",
            "longName": "Kalasatama(M)-Käpylä-Kannelmäki",
            "mode": "BUS"
          }
        },
        {
          "code": "HSL:1053:1:01",
          "directionId": 1,
          "headsign": "Arabia",
          "route": {
            "gtfsId": "HSL:1053",
            "shortName": "53",
            "longName": "Arabia-Oulunkylä-Maunula-Pohjois-Haaga-Konala-Uusmäki",
            "mode": "BUS"
          }
        },
        {
          "code": "HSL:1041:1:01",
          "directionId": 1,
          "headsign": "Kamppi",
          "route": {
            "gtfsId": "HSL:1041",
            "shortName": "41",
            "longName": "Kamppi-Pohjois-Haagan asema",
            "mode": "BUS"
          }
        }
      ]
    }
  }
}
```

Stop time HSL:1293133 Unix time "serviceDay": 1679176800, + "realtimeArrival": 61261, if not "scheduledArrival": 61740,

```
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

response

{
  "data": {
    "stop": {
      "name": "Ida Aalbergin tie",
      "stoptimesWithoutPatterns": [
        {
          "scheduledArrival": 61320,
          "realtimeArrival": 61261,
          "arrivalDelay": -59,
          "scheduledDeparture": 61320,
          "realtimeDeparture": 61279,
          "departureDelay": -41,
          "realtime": true,
          "realtimeState": "UPDATED",
          "serviceDay": 1679176800,
          "headsign": "Elielinaukio"
        },
        {
          "scheduledArrival": 61740,
          "realtimeArrival": 61756,
          "arrivalDelay": 16,
          "scheduledDeparture": 61740,
          "realtimeDeparture": 61771,
          "departureDelay": 31,
          "realtime": true,
          "realtimeState": "UPDATED",
          "serviceDay": 1679176800,
          "headsign": "Otaniemi via Huopalahti as."
        },
        {
          "scheduledArrival": 61920,
          "realtimeArrival": 61920,
          "arrivalDelay": 0,
          "scheduledDeparture": 61920,
          "realtimeDeparture": 61920,
          "departureDelay": 0,
          "realtime": false,
          "realtimeState": "SCHEDULED",
          "serviceDay": 1679176800,
          "headsign": "Kalasatama(M) via Käpylä as."
        },
        {
          "scheduledArrival": 62100,
          "realtimeArrival": 62100,
          "arrivalDelay": 0,
          "scheduledDeparture": 62100,
          "realtimeDeparture": 62100,
          "departureDelay": 0,
          "realtime": false,
          "realtimeState": "SCHEDULED",
          "serviceDay": 1679176800,
          "headsign": "Kamppi"
        },
        {
          "scheduledArrival": 62220,
          "realtimeArrival": 62220,
          "arrivalDelay": 0,
          "scheduledDeparture": 62220,
          "realtimeDeparture": 62220,
          "departureDelay": 0,
          "realtime": false,
          "realtimeState": "SCHEDULED",
          "serviceDay": 1679176800,
          "headsign": "Elielinaukio"
        }
      ]
    }
  }
}
```

