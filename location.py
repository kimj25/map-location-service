import zmq

def get_location_data(request):
    pass


def main():
    # set up ZeroMQ
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:[3010]")
    
    print("Map/Location Service is running...")
    
    while True:
        # wait for request
        message = socket.recv_string()
        print(f"Received request: {message}")
        
        # process request
        response = get_location_data(message)
        
        # send response
        socket.send_string(response)
        print(f"Sent response: {response}")

if __name__ == "__main__":
    main()