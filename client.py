import socket
import threading
import os
import random

COMMANDS = (
    '/get',
    '/connect',
    '/exit',
    '/help',
)

HELP_TXT = """
    '/get - get active connection list'
    '/connect <user> - connect to user in active connection list'
    '/exit - disconnect from user'
    '/help - show help',
"""

UDP_MAX_SIZE = 65535

def listen(s: socket.socket, host: str, port: int):
    while True:
        msg, addr = s.recvfrom(UDP_MAX_SIZE)
        msg_port = addr[-1]
        msg = msg.decode('utf-8')
        allowed_ports = threading.current_thread().allowed_ports
        if msg_port not in allowed_ports:
            continue

        if not msg:
            continue

        if '__' in msg:
            command, content = msg.split('__')
            if command == 'members':
                for n, members in enumerate(content.split(';'), start=1):
                    print('\r\r' + msg + '\n' + f'you: ', end='')
        else:
            peer_name = f'client{msg_port}'
            print('\r\r' + f'{peer_name}: '+ msg + '\n' + f'you: ', end='')

def start_listen(target, socked, host, port):
    th = threading.Thread(target=target, args=(socked, host, port), daemon=True)
    th.allowed_ports = []
    th.start()
    return th

def connect(host: str = '127.0.0.1', port: int = 3000):
    own_port = random.randint(8000, 9000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, own_port))

    listen_thread = start_listen(listen, s, host, port)
    allowed_ports = [port]
    listen_thread.allowed_ports = allowed_ports
    sendto = (host, port)
    s.sendto('__join'.encode('utf-8'), sendto)

    while True:
        msg = input(f'you: ')

        if msg in COMMANDS or msg.startswith('/connect'):
            if msg == '/get':
                s.sendto('/get'.encode('utf-8'), sendto)
            if msg.startswith('/connect'):
                peer = msg.split(' ')[-1]
                peer_port = int(peer.replace('client', ''))
                allowed_ports.append(peer_port)
                sendto = (host, peer_port)
                print(f'Connect to client{peer_port}')
            if msg == '/exit':
                peer_port = sendto[-1]
                allowed_ports.remove(peer_port)
                sendto = (host, port)
                print(f'Disconnect from client{peer_port}')
            if msg == '/help':
                print(HELP_TXT)
        else:
            s.sendto(msg.encode('utf-8'), sendto)

if __name__ == '__main__':
    os.system('cls')
    print('Welcome to chat!')
    connect()
