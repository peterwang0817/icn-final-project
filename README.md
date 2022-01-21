# Usage:
Our work provides two mode: video streaming, meet streaming. Video streaming will play a video, meet streaming will open your camera and microphone.

## Server
    cd ./Server/
    python Server.py 554

## Client
mode is chosen from video or meet

    cd ./Client/
    ./Client.bat <mode>
    
## Notes
After using SETUP, wait a few seconds before pressing play, or the audio may not load properly.
Our video is vague, for we use standard RTP queue size 1024, so we downsample our video, if we want higher resolution, we can simply increase the size of queue of both sender and reciever, and remove the downsampling procedures. 
