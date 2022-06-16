import threading

import zmq

from functions import collect_chat_room_input


def send():
    """
    Send(push) to the server thread.
    """

    while True:
        message = input()
        sender.send_string(f'{chat_room_number}{separator}{nickname}: {message}')


def receive():
    """
    Receive messages from the publisher thread.
    """
    while True:
        # Receives a msg and strips the chat room number and separator from it.
        message = subscriber.recv_string()
        sep_index = message.index(separator)
        clean_message = message[sep_index + 1:]
        print(f'{clean_message}')


if __name__ == '__main__':
    # Gets the nickname and chat room number from console.
    nickname = input('Enter your nickname: ')
    chat_room_number = collect_chat_room_input()
    # We use this symbol to separate the message from the unnecessary information to the client.
    separator = '>'

    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    # Each new subscriber subscribes with the chat room number selected and receives related topics only.
    subscriber.setsockopt_string(zmq.SUBSCRIBE, chat_room_number)
    subscriber.connect("tcp://localhost:5562")

    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://localhost:5563")

    # 2 Threads: one for send and one for receive.
    send_thread = threading.Thread(target=send)
    send_thread.start()

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
