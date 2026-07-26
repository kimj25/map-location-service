import zmq

def get_location_data(query):
    pass


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:3010") 
    
    print("Map/Location Service is running on port 3010...")
    print("Waiting for requests...") # message to show the service is running and waiting for requests
    
    while True:
        request = socket.recv_json()
        print(f"Received: {request}") # prints json request from the client
        
        query = request.get("query") # location query from the request eg) "Paris, France"
        response = get_location_data(query)
        
        socket.send_json(response)
        print(f"Sent: {response}")

if __name__ == "__main__":
    main()