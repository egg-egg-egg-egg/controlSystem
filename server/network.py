import socket
import threading
from shared.protocol import *

class ServerNetwork:
    def __init__(self, port=65432):
        self.clients = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', port))
        self.server.listen(5)

    def start_listening(self, callback):
        def handle_client(conn, addr):
            while True:
                try:
                    data = conn.recv(1024)
                    if data:
                        callback(addr[0], json.loads(data.decode()))
                except:
                    break
        
        listener = threading.Thread(target=self._accept_connections, args=(handle_client,))
        listener.start()

    def _accept_connections(self, handler):
        while True:
            conn, addr = self.server.accept()
            self.clients[addr[0]] = conn
            client_thread = threading.Thread(target=handler, args=(conn, addr))
            client_thread.start()