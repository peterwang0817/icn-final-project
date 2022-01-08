import socket
from debug import Generic

RTSP_PORT = 554
RTSP_BUFFER_SIZE = 1024

AUDIO_RTP_PORT = 8886
AUDIO_RCP_PORT = 8887
VIDEO_RTP_PORT = 8888
VIDEO_RCP_PORT = 8889

class RCPSocket(Generic):
    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        
        # create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._print_debug('Created UDP socket listening on port {0}'.format(self.port))
        self.socket.connect((host, port))



class RTSPClient(Generic):
    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        
        # create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._print_debug('Created TCP socket listening on port {0}'.format(self.port))
        self.socket.connect((host, port))
        
    def input_stream(self):
        return self.socket.recv(RTSP_BUFFER_SIZE).decode('utf-8')
    
    def output_stream(self, data):
        self.socket.send(data.encode('utf-8'))

    def RTSP_request(self, data):
        self.socket.send(data.encode('utf-8'))
        return self.socket.recv(RTSP_BUFFER_SIZE).decode('utf-8')

server_address = input('Enter server IP: ')
client = RTSPClient(server_address, RTSP_PORT)
cseq = 0

while True:
    input_msg = input('Enter command, or type "help": ').lower()
    response = ''

    if input_msg == 'help':
        print('options setup teardown play pause')
    elif input_msg == 'options':
        response = client.RTSP_request(('OPTIONS rtsp://example.com/media.mp4 RTSP/1.0\n'
                                        'CSeq: {0}\n'
                                        'Require: implicit-play\n'
                                        'Proxy-Require: gzipped-messages').format(cseq))
    elif input_msg == 'setup':
        response = client.RTSP_request(('SETUP rtsp://example.com/media.mp4/streamid=0 RTSP/1.0\n'
                                        'CSeq: {0}\n'
                                        'Transport: RTP/AVP;unicast;client_port={1}-{2}').format(cseq, VIDEO_RTP_PORT, VIDEO_RCP_PORT))
    elif input_msg == 'teardown':
        response = client.RTSP_request(('TEARDOWN rtsp://example.com/media.mp4 RTSP/1.0\n'
                                        'CSeq: {0}\n'
                                        'Session: 12345678').format(cseq))
    elif input_msg == 'play':
        response = client.RTSP_request(('PLAY rtsp://example.com/media.mp4 RTSP/1.0\n'
                                        'CSeq: {0}\n'
                                        'Range: npt=5-20\n'
                                        'Session: 12345678').format(cseq))
    elif input_msg == 'pause':
        response = client.RTSP_request(('PAUSE rtsp://example.com/media.mp4 RTSP/1.0\n'
                                        'CSeq: {0}\n'
                                        'Session: 12345678').format(cseq))
    else:
        print('Unknown command. Type "help" for a list of commands.')

    if response:
        print(response)
        cseq += 1