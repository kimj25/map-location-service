# map-location-service
Map/location microservice. Takes a location query (address, city, country, etc.) and returns coordinates, timezone, address details, and a Google Maps URL via ZeroMQ.

The service responds with JSON over ZeroMQ.
Needs internet connection - Nominatim geocoding API

## Dependencies
```
pip install pyzmq geopy timezonefinder
```

## Running the Service
```
python location.py
```
Runs a ZeroMQ REP socket on `tcp://*:3010`.

## Usage
Send a JSON request with a `query` field containing any location string:
```json
{"query": "Paris, France"}
{"query": "1234 Main St., New York, 10044"}
```

### Response (JSON)
```json
{
  "latitude": 48.8566,
  "longitude": 2.3522,
  "timezone": "Europe/Paris",
  "map_url": "https://www.google.com/maps?q=48.8566,2.3522",
  "city": "Paris",
  "state": "Île-de-France",
  "postcode": "75001",
  "country": "France",
}
```
Note: Some fields may be `null` depending on the location (e.g., searching by country won't return a `city`).

### Error Response
```json
{"error": "Missing required field: query"}
{"error": "Network error: Please check your connection and try again."}
```

### Example (Python client)
```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:3010")

socket.send_json({"query": "Tokyo, Japan"})
response = socket.recv_json()
print(response)
```
## UML Sequence Diagram
## UML Sequence Diagram

```mermaid
sequenceDiagram
    participant MP as Main Program
    participant MLS as Map/Location Service
    participant NOM as Nominatim API
    participant TF as TimezoneFinder

    MP->>MLS: send_json({"query": "Paris, France"})
    MLS->>NOM: geocode("Paris, France")
    
    alt Location found
        NOM-->>MLS: returns coordinates (lat, lng, address)
        MLS->>TF: timezone_at(lat, lng)
        TF-->>MLS: returns timezone string
        MLS->>MLS: build map_url from coordinates
        MLS-->>MP: send_json({latitude, longitude, timezone, map_url, city, ...})
    else Location not found
        NOM-->>MLS: returns None
        MLS-->>MP: send_json({"error": "Location not found"})
    else Network error
        NOM-->>MLS: ConnectionError/TimeoutError
        MLS-->>MP: send_json({"error": "Network error..."})
    else Missing query
        MLS-->>MP: send_json({"error": "Missing required field: query"})
    end
```
