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
    timezone = tf.timezone_at(lat=latitude, lng=longitude)
    
    # build map URL from coordinates
    map_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    
    # extract address details and extratags from raw response
    address = location.raw.get("address", {})
    extratags = location.raw.get("extratags", {})
    
    # return response as dictionary, each program can use the response dictionary to extract the required information
    return {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "map_url": map_url,
        "city": address.get("city"),
        "state": address.get("state"),
        "postcode": address.get("postcode"),
        "country": address.get("country"),
        "wikipedia": extratags.get("wikipedia")
    }


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:3010") 
    
    print("Map/Location Service is running on port 3010...")
    print("Waiting for requests...") # message to show the service is running and waiting for requests
    
    while True:
        request = socket.recv_json()
        print(f"Received: {request}") # prints json request from the client
        
        query = request.get("query") # get location from the request query eg) "Paris, France"
        response = get_location_data(query) # call the get_location_data function to get the location data based on the query
        
        socket.send_json(response) # send the response in json back to the client
        print(f"Sent: {response}")

if __name__ == "__main__":
    main()