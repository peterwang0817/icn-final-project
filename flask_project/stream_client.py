import socket
import threading
from RtpPacket import RtpPacket

INIT = 0
READY = 1
PLAYING = 2

SETUP = 0
PLAY = 1
PAUSE = 2
TEARDOWN = 3

CACHE_FILE_NAME = "cache"
CACHE_FILE_EXT = ".jpg"

class Client:

    state = INIT

    def __init__(self, filename, server_address, server_port, RTP_port):
        # basic variables
        self.server_address = server_address
        self.server_port = server_port
        self.RTP_port = RTP_port
        self.filename = filename

        # RTSP variables
        self.session_id = 0
        self.cseq = 0
        self.last_request_sent = -1
        self.teardown_ack = 0

        # sockets
        self.RTSP_socket = self._connect_server(self.server_address, self.server_port)
        self.RTP_socket = None

        self.current_frame = None
        self.frameNbr = 0

    def _print(self, s):
        print('[stream_client.py]: ' + s)

    def _open_RTP_port(self):
        """Open RTP socket binded to a specified port."""
        # Create a new datagram socket to receive RTP packets from the server
        self.RTP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Set the timeout value of the socket to 0.5sec
        self.RTP_socket.settimeout(0.5)

        try:
            # Bind the socket to the address using the RTP port given by the client user
            self.RTP_socket.bind(('', self.RTP_port))
            self._print('Listening for RTP on port {0}'.format(self.RTP_port))
        except:
            self._print('Unable to bind PORT={0}'.format(self.RTP_port))

    def _listen_RTP(self):        
        """Listen for RTP packets."""
        while True:
            try:
                data = self.RTP_socket.recv(20480)
                if data:
                    rtpPacket = RtpPacket()
                    rtpPacket.decode(data)
                    
                    currFrameNbr = rtpPacket.seqNum()
                    #self._print("Current Seq Num: {0}".format(currFrameNbr))
                    
                    if currFrameNbr > self.frameNbr: # Discard the late packet
                        self.frameNbr = currFrameNbr
                        
                        # self.updateAudio(self.writeAudio(rtpPacket.getPayload()))
                        self._write_frame(rtpPacket.getPayload())
                    
            except:
                # Stop listening upon requesting PAUSE or TEARDOWN
                if self.playEvent.isSet(): 
                    break
                
                # Upon receiving ACK for TEARDOWN request,
                # close the RTP socket
                if self.teardown_ack == 1:
                    self.RTP_socket.shutdown(socket.SHUT_RDWR)
                    self.RTP_socket.close()
                    break

    def _write_frame(self, data):
        """Write the received frame to a temp image file. Return the image file."""
        cache_name = CACHE_FILE_NAME + str(self.session_id) + CACHE_FILE_EXT
        file = open(cache_name, "wb")
        file.write(data)
        file.close()
		
        return cache_name

    def _connect_server(self, address, port):
        """Connects to server using a TCP socket."""
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            new_socket.connect((address, port))
            self._print('Connected to server {0} succesfully.'.format(address))
        except:
            self._print('Connection to {0} failed.'.format(address))
        return new_socket

    def _parse_RTSP_response(self, data):
        """Parses a RTSP response."""
        lines = data.split('\n')
        session_cseq = int(lines[1][6:])

        if session_cseq == self.cseq:
            session = int(lines[2].split(' ')[1]) # is this correct?
            # Accept new RTSP session
            if self.session_id == 0:
                self.session_id = session
            # Process only if session ID is the same
            if self.session_id == session:
                    if self.last_request_sent == SETUP:
                        # Update RTSP state.
                        self.state = READY
                        
                        # Open RTP port.
                        self._open_RTP_port() 
                    elif self.last_request_sent == PLAY:
                        self.state = PLAYING
                        
                    elif self.last_request_sent == PAUSE:
                        self.state = READY
                        
                        # The play thread exits. A new thread is created on resume.
                        self.playEvent.set()
                    elif self.last_request_sent == TEARDOWN:
                        self.state = INIT
                        
                        # Flag the teardownAcked to close the socket.
                        self.teardown_ack = 1 

    def _recv_RTSP_response(self):
        """Receives RTSP response from a server."""
        while True:
            response = self.RTSP_socket.recv(1024)

            if response:
                self._parse_RTSP_response(response.decode("utf-8"))

            # Close the RTSP socket upon requesting Teardown
            if self.last_request_sent == TEARDOWN:
                self.RTSP_socket.shutdown(socket.SHUT_RDWR)
                self.RTSP_socket.close()
                break

    def _send_RTSP_request(self, request_type):
        request = ''

        if request_type == SETUP and self.state == INIT:
            threading.Thread(target=self._recv_RTSP_response).start()
            self.cseq += 1
            request = ('SETUP {0} RTSP/1.0\n'
                       'CSeq: {1}\n'
                       'Transport: RTP/AVP; client_port= {2}').format(self.filename, self.cseq, self.RTP_port)
            self.last_request_sent = SETUP

        elif request_type == PLAY and self.state == READY:
            self.cseq += 1
            request = ('PLAY {0} RTSP/1.0\n'
                       'CSeq: {1}\n'
                       'Session: {2}').format(self.filename, self.cseq, self.session_id)
            self.last_request_sent = PLAY

        elif request_type == PAUSE and self.state == PLAYING:
            self.cseq += 1
            request = ('PAUSE {0} RTSP/1.0\n'
                       'CSeq: {1}\n'
                       'Session: {2}').format(self.filename, self.cseq, self.session_id)
            self.last_request_sent = PAUSE

        elif request_type == TEARDOWN and not self.state == INIT:
            self.cseq += 1
            request = ('TEARDOWN {0} RTSP/1.0\n'
                       'CSeq: {1}\n'
                       'Session: {2}').format(self.filename, self.cseq, self.session_id)
            self.last_request_sent = TEARDOWN
        else:
            return

        self.RTSP_socket.send(request.encode('utf-8'))
        self._print('RTSP request sent:\n\n{0}\n'.format(request))

    def setup(self):
        """PUBLIC METHOD CALLED BY FLASK. Sets up streaming session."""
        if self.state == INIT:
            self._send_RTSP_request(SETUP)

    def play(self):
        """PUBLIC METHOD CALLED BY FLASK. Plays/resumes streaming session."""
        if self.state == READY:
            # Create a new thread to listen for RTP packets
            threading.Thread(target=self._listen_RTP).start()
            self.playEvent = threading.Event()
            self.playEvent.clear()
            self._send_RTSP_request(PLAY)

    def pause(self):
        """PUBLIC METHOD CALLED BY FLASK. Pauses streaming session."""
        if self.state == PLAYING:
            self._send_RTSP_request(PAUSE)

    def teardown(self):
        """PUBLIC METHOD CALLED BY FLASK. Tears down streaming session."""
        self._send_RTSP_request(TEARDOWN)       
        #os.remove(CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT) # Delete the cache image from video