import socket
import sys

class ClientSocket:
    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        
        # create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._print_debug('Created socket listening on port {0}'.format(self.port))
        self.socket.connect((host, port))
        
    def input_stream(self):
        return self.socket.recv(1024).decode('utf-8')
    
    def output_stream(self, data):
        self.socket.send(data.encode('utf-8'))
        
    def _print(self, s):
        print('[CLIENT]: {0}'.format(s))
        
    def _print_debug(self, s):
        if self.debug: self._print(s)


if __name__ == "__main__":
    input_valid = True
    try: 
        server_address, server_port = str(sys.argv[1]), int(sys.argv[2])
    except:
        input_valid = False
        print('incorrect input')
        
    if input_valid:
        print('trying to connect to {0}:{1}'.format(server_address, server_port))
        client = ClientSocket(server_address, server_port, debug=True)
    
        while True:
            response = input(client.input_stream())
            #client.output_stream('OPTIONS rtsp://example.com/media.mp4 RTSP/1.0\nCSeq: 1\nRequire: implicit-play\nProxy-Require: gzipped-messages')
            client.output_stream('SETUP rtsp://example.com/media.mp4/streamid=0 RTSP/1.0\nCSeq: 3\nTransport: RTP/AVP;unicast;client_port=8000-8001')
