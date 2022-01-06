import socket
import threading
import cv2

SERVER_IP = '127.0.0.1'
SERVER_PORT = 554

BUFFER_SIZE = 1024

class Generic:
    """Generic class that implements basic debugging and printing. All objects that use print should inherit from this class.\n
    Methods:\n
    _print(string): prints a string to console, regardless of whether debug is toggled.
    _print_debug(string): prints a string to console, if debug is on.
    """
    def __init__(self, debug=False):
        self.name = 'RTSP Request Handler'
        self.debug = debug
        
    def _print(self, s):
        print('[{0}]: {1}'.format(self.name, s))
        
    def _print_debug(self, s):
        if self.debug: self._print(s)


class RTSP_RequestHandler(Generic):
    """Handles all RTSP requests, controls the RTP socket, and creates RTSP responses.\n
    Currently supports the following requests:\n
    OPTIONS
    """
    def __init__(self, debug=False):
        self.name = 'RTSP Request Handler'
        self.debug = debug

    def response(self, RTSP_request):
        header = RTSP_request.split('\n')
        # 1st line of RTSP request, example below
        # SETUP rtsp://example.com/media.mp4/streamid=0 RTSP/1.0
        request, url, version = header[0].split(' ')
        # 2nd line of RTSP request, example below
        # CSeq: 3
        cseq = int(header[1][6:])

        self._print_debug('request type:"{0}", url:"{1}", version:"{2}", cseq:"{3}"'.format(request, url, version, cseq))
        
        # build the RTSP response
        RTSP_response = 'RTSP/1.0 200 OK\nCseq: {0}\n'.format(cseq)
        if request == 'OPTIONS':
            RTSP_response += self._options()
        elif request == 'SETUP':
            RTSP_response += self._setup()
        elif request == 'TEARDOWN':
            RTSP_response += self._teardown()
        elif request == 'PLAY':
            RTSP_response += self._play()
        elif request == 'PAUSE':
            RTSP_response += self._pause()
        else:
            RTSP_response = 'RTSP/1.0 400 Bad_Request\nCseq: {0}\n'.format(cseq)
        return RTSP_response

    def _options(self):
        return 'Public: DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE\n'

    def _setup(self, header):
        protocol, cast, client_port_range = (header[2][11:]).split(';')
        self._print_debug('protocol:"{0}", cast:"{1}", client_port:"{2}"'.format(protocol, cast, client_port_range))
        session_number = 1234
        # TODO: setup session
        return 'Transport: {0};{1};{2}\nSession: {3}\n'.format(protocol, cast, client_port_range, session_number)

    def _teardown(self, header):
        session_number = int(header[2][8:])
        self._print_debug('teardown session num:"{0}"'.format(session_number))
        # TODO: teardown session
        return ''

    def _play(self, header):
        # TODO: play
        # TODO (easy): build PLAY RTSP response
        return ''

    def _pause(self, header):
        # TODO: pause
        # TODO (easy): build PAUSE RTSP response
        return ''


class ClientThread(Generic):
    """A ClientThread is created for each client connection to the server. Waits for RTSP requests from
    the client and passes them to the RTSP_RequestHandler.
    """
    def __init__(self, client_socket, address, debug=False):
        self.name = 'Client {0}:{1}'.format(address[0], address[1]) # [IP address]:[port]
        self.client_socket = client_socket
        self.debug = debug
        self.RTSP_handler = RTSP_RequestHandler()
        
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
        self.output_stream(self.RTSP_handler.response(data))
        
    def input_stream(self):
        return self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
    
    def output_stream(self, data):
        self.client_socket.send(data.encode('utf-8'))


class ServerSocket(Generic):
    """Waits for TCP connections from clients, and then initiates ClientThreads to interact with each client.
    """
    def __init__(self, host=SERVER_IP, port=SERVER_PORT, debug=False):
        self.name = 'Server Socket'
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
        
if __name__ == "__main__":
    server = ServerSocket(SERVER_IP, SERVER_PORT, debug=True)