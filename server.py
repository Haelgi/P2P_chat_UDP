import socket

class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3000

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.port))
        print(f'Listening at {self.host}:{self.port}')

        self.conn_list=[]
        self.run()

    def run(self):
        while True:
            msg, addr = self.s.recvfrom(1024)

            if addr not in self.conn_list:
                self.conn_list.append(addr)
            
            if not msg:
                continue

            if msg.decode('ascii') == '__join':
                print(f'Client {addr[1]} joined chat')
                continue

            msg = f'client{addr[1]}: {msg.decode('ascii')}'

            for conn in self.conn_list:
                if conn == addr:
                    continue

                self.s.sendto(msg.encode('ascii'), conn)

if __name__ == '__main__':
    Server()
