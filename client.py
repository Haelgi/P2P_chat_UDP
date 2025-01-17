import socket
import threading
import os

class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3000

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.connect((self.host, self.port))

        threading.Thread(target=self.listen, args=(self.s,), daemon=True).start()

        self.s.send('__join'.encode('utf-8'))
        self.run()

    def run(self):
        while True:
            msg = input(f'you: ')
            self.s.send(msg.encode('utf-8'))
    
    def listen(self, s: socket.socket):
        while True:
            msg = self.s.recv(1024)
            print('\r\r' + msg.decode('utf-8') + '\n' + f'you: ', end='')

if __name__ == '__main__':
    os.system('cls')
    print('Welcom to chat!')
    Client()


        