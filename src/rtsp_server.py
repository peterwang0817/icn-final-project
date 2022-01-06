import socket
import threading
import cv2

SERVER_IP = '127.0.0.1'
SERVER_PORT = 554

BUFFER_SIZE = 1024

class ClientThread:
    def __init__(self, client_socket, address, debug=False):
        self.client_socket = client_socket
        self.name = '{0}:{1}'.format(address[0], address[1]) # [IP address]:[port]
        self.debug = debug
        
        self.client_socket.send('Welcome to the server\n'.encode('utf-8'))
        
        # listen for data from socket
        while True:
            data = self.input_stream()
            if not data:
                break
            self._main(data)
        self.client_socket.close()
        self._print_debug('Disconnected')
        
    def _main(self, data):
        header = data.split('\n')
        request, url, version = header[0].split(' ')
        cseq = int(header[1][6:])
        self._print('request type:"{0}", url:"{1}", version:"{2}", cseq:"{3}"'.format(request, url, version, cseq))
        
        # build the RTSP response
        response = 'RTSP/1.0 200 OK\nCseq: {0}\n'.format(cseq)

        if request == 'OPTIONS':
            response += 'Public: DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE\n'

        elif request == 'SETUP':
            protocol, cast, client_port_range = (header[2][11:]).split(';')
            self._print('protocol:"{0}", cast:"{1}", client_port:"{2}"'.format(protocol, cast, client_port_range))
            session_number = 1234
            # TODO: setup session
            response += 'Transport: {0};{1};{2}\n'.format(protocol, cast, client_port_range)
            response += 'Session: {0}\n'.format(session_number)

        elif request == 'TEARDOWN':
            session_number = int(header[2][8:])
            self._print('teardown session num:"{0}"'.format(session_number))
            # TODO: teardown session

        elif request == 'PLAY':
            # TODO: play
            # TODO (easy): build PLAY RTSP response
            pass

        elif request == 'PAUSE':
            # TODO: pause
            # TODO (easy): build PAUSE RTSP response
            pass

        else:
            response = 'RTSP/1.0 400 BadRequest\nCseq: {0}\n'.format(cseq)
        
        self.output_stream(response)
        
    def input_stream(self):
        return self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
    
    def output_stream(self, data):
        self.client_socket.send(data.encode('utf-8'))
        
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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._print_debug('Created TCP socket listening on port {0}'.format(self.port))
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
    server = ServerSocket(SERVER_IP, SERVER_PORT, debug=False)