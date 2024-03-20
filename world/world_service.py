import selectors
import socket
import sys
import traceback

from message.client_message import ClientMessage
from message.server_message import ServerMessage
from world.map import Map

WORLD_HOST = '127.0.0.1'
WORLD_PORT = 0
DISCOVERY_HOST = '127.0.0.1'
DISCOVERY_PORT = 0
DEBUG = True


def main():
    register_service()
    map = Map()
    game(map)


def register_service():
    """
    register the world service with the discovery service
    :return:
    """
    action = {
        'action': 'register',
        'ip': WORLD_HOST,
        'port': WORLD_PORT,
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
                        f'World: Error: Exception for {message.ipaddr}:\n'
                        f'{traceback.format_exc()}'
                    )
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print('World: Caught keyboard interrupt, exiting')
    finally:
        sel.close()
    print(message.response)


def create_world(hive_count):
    return []


def show_area(xcoord, ycoord, range):
    return []


def show_map():
    return []


def game(map):
    """
    process the rounds of the game
    :param map  the world map
    :return:
    """
    sel = selectors.DefaultSelector()
    host = WORLD_HOST
    port = WORLD_PORT

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    print(f'World: Listening on {(host, port)}')
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(sel, key.fileobj)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)
                        process_action(message, map)
                    except Exception:
                        print(
                            f'World: Error: Exception for {message.ipaddr}:\n'
                            f'{traceback.format_exc()}'
                        )
                        message.close()
    except KeyboardInterrupt:
        if DEBUG == '1': print('World: Caught keyboard interrupt, exiting')
    finally:
        sel.close()


def process_action(message, map):
    """

    :param message:
    :param map:
    :return:
    """
    if DEBUG == '1': print(f'World: message.event={message.event}')
    if message.event == 'READ':
        action = message.request['action']
        if action == 'new':
            hive_locations = create_world(message.request['count'])
            message.response = hive_locations
        elif action == 'area':
            area = show_area(
                message.request['xcoord'],
                message.request['ycoord'],
                message.request['range'],
            )
        elif action == 'map':
            pass

        message.set_selector_events_mask('w')


def create_request(action_item):
    """
    creates the body of the request
    :param action_item:
    :return:
    """
    return dict(
        type='text/json',
        encoding='utf-8',
        content=action_item,
    )


def start_connection(sel, host, port, request):
    """
    starts the connection to a remote socket
    :param sel:
    :param host:
    :param port:
    :param request:
    :return:
    """
    addr = (host, port)
    if DEBUG: print(f'Hive1: Starting connection to {addr}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = ClientMessage(sel, sock, addr, request)
    sel.register(sock, events, data=message)


def accept_wrapper(sel, sock):
    """
    Wrapper for the recieved messages
    :param sel:
    :param sock:
    :return:
    """
    conn, addr = sock.accept()  # Should be ready to read
    if DEBUG: print(f'Hive1: Accepted connection from {addr}')
    conn.setblocking(False)
    message = ServerMessage(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Script needs two arguments')
        exit(2)
    else:
        DISCOVERY_PORT = int(sys.argv[1])
        WORLD_PORT = int(sys.argv[2])
        main()
