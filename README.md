# Usage:
    Server: python Server.py <rstp port>
    Client: python ClientLauncher.py <server ip> <rstp port> <rtp port> <file name>
    OR: use webpage (run flask_project/quick_debug.bat)

    rstp port is usually 554, rtp port 25000, for server ip, you can just use localhosts
    file name:
        end with .mp4, .Mjpeg or live (for camera shoting)


    flask_project issues:
    - cached images are not removed
    - no proper teardown
    - stream turns white at times (packet loss?)