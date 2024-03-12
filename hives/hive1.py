import json
import random
import selectors
import socket
import traceback

from message.client_message import ClientMessage
from message.server_message import ServerMessage

ANTHILL_HOST = '127.0.0.1'
ANTHILL_PORT = 62222
DISCOVERY_HOST = '127.0.0.1'
DISCOVERY_PORT = 61111
DEBUG = True


def main():
    register()
    game()


def register():
    """
    register this anthill services with the discovery service
    :return:
    """
    action = {
        'action': 'register',
        'ip': ANTHILL_HOST,
        'port': ANTHILL_PORT,
        'type': 'hive'
    }

    sel = selectors.DefaultSelector()
    request = create_request(action)
    start_connection(
        sel,
        DISCOVERY_HOST,
        DISCOVERY_PORT,
        request
    )

    message = None
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        f'Anthill1: Error: Exception for {message.ipaddr}:\n'
                        f'{traceback.format_exc()}'
                    )
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print('Anthill1: Caught keyboard interrupt, exiting')
    finally:
        sel.close()
    if DEBUG: print(message)


def game():
    """
    process the rounds of the game
    :return:
    """
    sel = selectors.DefaultSelector()
    host = ANTHILL_HOST
    port = ANTHILL_PORT

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    if DEBUG: print(f'Hive1: Listening on {(host, port)}')
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    playing = True
    try:
        while playing:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(sel, key.fileobj)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)
                        process_action(message)
                    except StopIteration:
                        if DEBUG: print(f'Hive1: Game over')
                        playing = False
                    except Exception:
                        print(
                            f'Hive1: Error: Exception for {message.ipaddr}:\n'
                            f'{traceback.format_exc()}'
                        )
                        message.close()
    except KeyboardInterrupt:
        if DEBUG: print('Hive1: Caught keyboard interrupt, exiting')

    finally:
        sel.close()


def create_request(action_item):
    return dict(
        type='text/json',
        encoding='utf-8',
        content=action_item,
    )


def start_connection(sel, host, port, request):
    addr = (host, port)
    if DEBUG: print(f'Anthill1: Starting connection to {addr}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = ClientMessage(sel, sock, addr, request)
    sel.register(sock, events, data=message)


def process_action(message):
    """
    process the action from the game service
    :param message:
    :return:
    """
    if DEBUG: print(f'Anthill1: message.event={message.event}')
    if message.event == 'READ':
        action = message.request['action']
        if action == 'quit':
            message.response = 'OK'
        elif action == 'round':
            directions = ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE', 'H']
            moves = random.choices(directions, k=message.request['count'])
            ''' only for debugging '''
            #moves.pop()
            #moves.append('H')
            #moves[0] = 'X'
            ''' only for debugging '''
            message.response = json.dumps(moves)
        message.set_selector_events_mask('w')
    else:
        action = message.request['action']
        if action == 'quit':
            raise StopIteration


def accept_wrapper(sel, sock):
    conn, addr = sock.accept()  # Should be ready to read
    if DEBUG: print(f'Anthill1: Accepted connection from {addr}')
    conn.setblocking(False)
    message = ServerMessage(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


if __name__ == '__main__':
    main()
