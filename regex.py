import re

data = ('RTSP/1.0 200 OK\n'
        'CSeq: 3\n'
        'Transport: RTP/AVP;unicast;client_port=8000-8001;server_port=9000-9001;ssrc=1234ABCD\n'
        'Session: 12345678\n')

m = re.search('^The.*Spain$', 'The rain in Spain')

p = re.compile('^Transport.*\n$')

print(p.findall(data))