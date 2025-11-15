from FlightRadar24 import FlightRadar24API
import datetime
from dotenv import load_dotenv
import os

# get login
load_dotenv()
username = os.getenv("FR24_USERNAME")
password = os.getenv("FR24_PASSWORD")

# object to start fetching data
fr_api = FlightRadar24API()
if not fr_api.is_logged_in():
    fr_api.login(username, password)
config = fr_api.get_flight_tracker_config()
config.limit = "10"

if __name__ == "__main__":
    flights = fr_api.get_flights()
    print(fr_api.get_history_data(flights[0],"CSV", datetime.datetime.now()))
    # flight_time = datetime.datetime.fromtimestamp(flights.get_flight("").time.scheduled.departure)
    # print(flight_time)

