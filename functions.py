def collect_chat_room_input():
    # Ensures chat rooms are numbers only
    value = input('Enter chat room number: ')
    try:
        int(value)
    except ValueError:
        print("Please enter integer value!")
        return collect_chat_room_input()

    return value


