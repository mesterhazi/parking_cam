# This script tested for use with Python 3
# This script starts a web server, so needs to be run as root or using sudo
# This application will be available by accessing http://<your raspberry pi ip address>:5000

from flask import Flask, Response, render_template
import cv2
import threading
import sys
import time
from copy import copy

# Initialise Flask, the Python web server package which serves all of this up to a browser
app = Flask(__name__)

# Define global variables for future use
# They are initialized to None so that we can confirm they have been set up later
frame_lock = threading.Lock()
frame = None
camera = None


# Setup function to set up camera, motors - only runs once, but nice to have them all contained in one place
def setup():

    global camera

    try:
        camera = cv2.VideoCapture(0)
    except Exception:
        # If there is an error, make sure we clean up any pin assignments
        cleanup()


# Cleanup function to release the camera and GPIO pins ready for the next time
def cleanup():

    print('Done, cleaning up video and GPIO')
    camera.release()
    cv2.destroyAllWindows()
    sys.exit("Cleaned up") # Make sure the application exits after a cleanup in case it was called due to an error


# Function to generate frames from the camera using the cv2 library
def generateFrames(fps=30):  # generate frame by frame from camera
    global frame_lock
    global frame
    act_frame = None

    while True:
        with frame_lock:
            act_frame = copy(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + act_frame + b'\r\n')  # Concat frame one by one and show result
        time.sleep(1 / fps)

# @app.route decorators tell flask which functions return HTML pages
# Video streaming route - should output an the live video stream
# A note to that Reddit commenter - unfortunately latency wasn't a consideration here - it's probably pretty laggy
@app.route('/video_feed')
def video_feed():
    return Response(generateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def read_frames(source):
    global frame_lock
    global frame
    act_frame = None

    while True:
        ret, buffer = source.read()
        ret, buffer = cv2.imencode('.jpg', buffer)
        if ret:
            act_frame = buffer.tobytes()
            with frame_lock:
                frame = copy(act_frame)
        else:
            time.sleep(1)

# Main/index route - the page that loads when you access the app via a browser
@app.route('/')
def index():
    return render_template('easy_index.html')


# Launch the Flask web server when this script is executed
# Catch KeyboardInterrupt so that if the application is quitting, cleanup can be run
try:

    if __name__ == '__main__': # If the script is being run directly rather than called by another script

        setup()
        image_thread = threading.Thread(target=read_frames, args=(camera, ), daemon=True)
        image_thread.start()
        # Start the flask app!
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        
except KeyboardInterrupt:

    pass

finally:

    # Ensure cleanup on exit
    cleanup()

# End of file!