import socket
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8888

BUFFER_SIZE = 1024

class ClientThread:
    def __init__(self, client_socket, address, debug=False):
        self.client_socket = client_socket
        self.name = '{0}:{1}'.format(address[0], address[1]) # [IP address]:[port]
        self.debug = debug
        
        self.client_socket.send('Welcome to the server\n'.encode())
        
        # listen for data from socket
        while True:
            data = self.client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            self._main(data)
        self.client_socket.close()
        self._print_debug('Disconnected')
        
    def _main(self, data):
        print(data)
        
    def input_stream(self, data):
        return self.socket.recv(1024).decode('utf-8')
    
    def output_stream(self, data):
        self.socket.send(data.encode('utf-8'))
        
    def _print(self, s):
        print('[{0}]: {1}'.format(self.name, s))
        
    def _print_debug(self, s):
        if self.debug: self._print(s)

    
class ServerSocket:
    def __init__(self, host=SERVER_IP, port=SERVER_PORT, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        
        # create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._print_debug('Created socket listening on port {0}'.format(self.port))
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
    
        # loop to accept connections
        while True:
            try:
                (client_socket, address) = self.socket.accept()
            except:
                self._print('An exception occured while listening for connections')
                
            # handle connection as client thread
            thread = threading.Thread(target=ClientThread, args=(client_socket, address))
            thread.setDaemon = True
            thread.start()
    
    # return number of client connections
    def get_active_connections(self):
        return threading.active_count() - 1 # subtract one for main thread
            
    def shutdown(self):
        self.socket.close()
        self._print('Socket was closed.')
        
    def _print(self, s):
        print('[SERVER]: {0}'.format(s))
        
    def _print_debug(self, s):
        if self.debug: self._print(s)
        
if __name__ == "__main__":
    server = ServerSocket(SERVER_IP, SERVER_PORT, debug=True)