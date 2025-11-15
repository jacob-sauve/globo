from FlightRadar24 import FlightRadar24API

# object to start fetching data
fr_api = FlightRadar24API()

flights = fr_api.get_flights()
print(flights)