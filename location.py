from datetime import datetime
from zoneinfo import ZoneInfo
import zmq
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def get_location_data(query):
    """get coordinates and timezone using python libraries geopy, timezonefinder
     and nomainatim API from input location query.
     Returns a dictionary with latitude, longitude, timezone, and map URL."""

    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="map_location_service")

    # get location's coordinates from any input format (address, city, country, etc.)
    location = geolocator.geocode(query, addressdetails=True, extratags=True)

    # if location not found, return error
    if location is None:
        return {"error": "Location not found. Please try again."}

    latitude= location.latitude
    longitude= location.longitude

    # for debugging purpose
    print(location.address)
    print((latitude, longitude))

    # get timezone from coordinates
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    # get timezone abbreviation (e.g., PST, EST, etc.)
    timezone_abbrev = datetime.now(ZoneInfo(timezone_str)).strftime('%Z')

    # build map URL from coordinates
    map_url = f"https://www.google.com/maps?q={latitude},{longitude}"

    # extract address details and extratags from raw response
    address = location.raw.get("address", {})

    # return response in dictionary, each program can extract the required information
    return {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone_abbrev,
        "map_url": map_url,
        "city": address.get("city"),
        "state": address.get("state"),
        "postcode": address.get("postcode"),
        "country": address.get("country")
    }


def main():
    """Main function to run the ZeroMQ server 
    that listens for location queries and responds with location data."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:3010")

    print("Map/Location Service is running on port 3010...")
     # message to show the service is running and waiting for requests
    print("Waiting for requests...")

    while True:
        request = socket.recv_json()
        print(f"Received: {request}") # prints json request from the client

        query = request.get("query") # get location from the request query eg) "Paris, France"
        # call the get_location_data function to get the location data based on the query
        response = get_location_data(query)

        socket.send_json(response) # send the response in json back to the client
        print(f"Sent: {response}")

if __name__ == "__main__":
    main()
