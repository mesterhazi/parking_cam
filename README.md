# parking_cam

## Goal
The ultimate goal is to use a cheap wide angle parking camera and stream its image to a mobile phone. Preferably without a special app on the phone. 
For this I use:
 - A cheap parking camera with composite video output
 - An Easycap like usb capture device (with stk1160 chip)
 - A raspberry pi (3B+ for now)
## How to do it: ffmpeg + websocket + jsmpeg
This method uses ffmpeg and a javascript based MPEG1 player as described by [phoboslab](https://github.com/phoboslab/jsmpeg).
#### ffmpeg
ffmpeg can use v4l2 devices  encode the video and stream to a given websocket address. In this case ffmpeg had to be built from source with the fix mentioned [here](https://www.raspberrypi.org/forums/viewtopic.php?t=270023#p1638521)). 

    git clone git://source.ffmpeg.org/ffmpeg.git ffmpeg
    cd ffmpeg
    # apply the change in v4l2.c as described above
    ./configure
    make -j4
    sudo make install
#### JSMpeg
Follow the instructions from [phoboslab/jsmpeg- Example setup](https://github.com/phoboslab/jsmpeg#example-setup-for-streaming-raspberry-pi-live-webcam))

