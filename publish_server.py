import time

import zmq


def main():
    context = zmq.Context()
    # The server plays a publisher part to all subs.
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5562")
    # It also pulls messages from the all the clients
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://*:5563")

    # Gives the server time to connect
    time.sleep(1)

    print('Server is running')

    while True:
        # The server receives messages from the pull socket
        message = receiver.recv().decode()
        # The first symbol in the message is the chat room number
        print(f'message received {message}')

        # It then sends it to all subscribers, each subscriber is filtering by chat room number
        publisher.send_string(f"{message}")


if __name__ == '__main__':
    main()
