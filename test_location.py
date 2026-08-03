import zmq

def test_location_service():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:3010") # connects to the location service via 3010 port

    # test 1: valid city and country
    print("Test 1: Valid city and country")
    socket.send_json({"query": "Paris, France"}) # send request to the location service
    response = socket.recv_json()   # receive response from the location service
    print(f"Response: {response}")  # shows the data
    print()

    # test 2: valid full address
    print("Test 2: Full address")
    socket.send_json({"query": "1600 Amphitheatre Parkway, Mountain View, CA"})
    response = socket.recv_json()
    print(f"Response: {response}")
    print()

    # test 3: invalid location
    print("Test 3: Invalid location")
    socket.send_json({"query": "Blahblah, Fakecountry"})
    response = socket.recv_json()
    print(f"Response: {response}")
    print()

    # test 4: missing query
    print("Test 4: Missing query")
    socket.send_json({})
    response = socket.recv_json()
    print(f"Response: {response}")
    print()

    # test 6: domestic US address
    print("Test 6: Domestic US city")
    socket.send_json({"query": "Portland, Oregon"})
    response = socket.recv_json()
    print(f"Response: {response}")
    print()

    # test 7: venue/landmark name
    print("Test 7: Landmark")
    socket.send_json({"query": "Eiffel Tower, Paris"})
    response = socket.recv_json()
    print(f"Response: {response}")
    print()

    # test 8: empty string
    print("Test 8: Empty string")
    socket.send_json({"query": ""})
    response = socket.recv_json()
    print(f"Response: {response}")
    print()

    socket.close()
    context.term()

if __name__ == "__main__":
    test_location_service()