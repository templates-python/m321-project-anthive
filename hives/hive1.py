import selectors
import socket

from message.client_message import ClientMessage
from message.server_message import ServerMessage
from discovery.services import Services

ANTHILL_HOST = '127.0.0.1'
ANTHILL_PORT = 62169 # 62000 - 62999
DISCOVERY_HOST = '127.0.0.1'
DISCOVERY_PORT = 61111
DEBUG = True


def main():
    register()
    game()


def register():
    """
    register this anthill service with the discovery service
    :return: None
    """
    sel = selectors.DefaultSelector()
    item = {'action': 'register', 'ip': ANTHILL_HOST, 'port': ANTHILL_PORT, 'type': 'hive'}
    request = create_request(item)
    start_connection(sel, DISCOVERY_HOST, DISCOVERY_PORT, request)

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        f'Main: Error: Exception for {message.ipaddr}:\n'
                        #f'{traceback.format_exc()}'
                    )
                    message._close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print('Caught keyboard interrupt, exiting')
    finally:
        sel.close()
    print(message)


def game():
    """
    process the rounds of the game
    :return:
    """
    sel = selectors.DefaultSelector()
    services = Services()

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((ANTHILL_HOST, ANTHILL_PORT))
    lsock.listen()
    print(f'Listening on {(ANTHILL_HOST, ANTHILL_PORT)}')
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
                        process_action(message, services)
                    except Exception:
                        print(
                            f'Main: Error: Exception for {message.ipaddr}:\n'
                            #f'{traceback.format_exc()}'
                        )
                        message._close()
    except KeyboardInterrupt:
        print('Caught keyboard interrupt, exiting')
    finally:
        sel.close()

def process_action(message):
    """
    process the action from the game service
    :param message:
    :return:
    """
    if message.event == 'READ':
        action = message.request['action']

        if action == 'register':
            message.response = Services.register(message.request['type'], message.request['ip'],message.request['port'])
        elif action == 'heartbeat':
            message.response = Services.heartbeat(message.request['uuid'])
        elif action == 'query':
            message.response = Services.query(message.request['type'])
        else:
            message.response = 'TODO Repsonse from the method'



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
    main()
