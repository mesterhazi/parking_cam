# This script tested for use with Python 3
# This script starts a web server, so needs to be run as root or using sudo
# This application will be available by accessing http://<your raspberry pi ip address>:5000

from flask import Flask, Response, render_template
import cv2
import threading
import sys

# Initialise Flask, the Python web server package which serves all of this up to a browser
app = Flask(__name__)

# Define global variables for future use
# They are initialized to None so that we can confirm they have been set up later

global camera
camera = None

# Setup function to set up camera, motors - only runs once, but nice to have them all contained in one place
def setup():

    global camera
    
    
    try:
        camera = cv2.VideoCapture(0)
    except:
        # If there is an error, make sure we clean up any pin assignments
        cleanup()

# Cleanup function to release the camera and GPIO pins ready for the next time
def cleanup():

    print('Done, cleaning up video and GPIO')
    camera.release()
    cv2.destroyAllWindows()
    sys.exit("Cleaned up") # Make sure the application exits after a cleanup in case it was called due to an error

# Function to generate frames from the camera using the cv2 library
def generateFrames():  # generate frame by frame from camera

    # Ensure the global camera variable is used in this scope
    global camera

    # Only try to generate frames if the camera variable has been populated
    if camera:
        while True:
            # Capture frame
            success, frame = camera.read()  # Reads the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Concat frame one by one and show result

# @app.route decorators tell flask which functions return HTML pages

# Video streaming route - should output an the live video stream
# A note to that Reddit commenter - unfortunately latency wasn't a consideration here - it's probably pretty laggy
@app.route('/video_feed')
def video_feed():
    return Response(generateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Main/index route - the page that loads when you access the app via a browser
@app.route('/')
def index():
    return render_template('easy_index.html') # Ensure that index.html exists in the templates subdirectory for this to work



# Launch the Flask web server when this script is executed
# Catch KeyboardInterrupt so that if the application is quitting, cleanup can be run
try:

    if __name__ == '__main__': # If the script is being run directly rather than called by another script

        # Make sure setup only runs once at launch, otherwise you'll get errors as the camera/GPIO are already in use
        setup() 

        # Start the flask app!
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        # App is run WITHOUT threading to reduce the chance of camera/GPIO conflict - only one concurrent user is expected, so this is fine
        # Debug is enabled so we can see what's happening in the console
        # However, the app automatically reloads when debug=True, which causes camera/GPIO conflicts, so this is disabled with use_reloader=false
        # This application will be available by accessing http://<your raspberry pi ip address>:5000

except KeyboardInterrupt:

    pass

finally:

    # Ensure cleanup on exit
    cleanup()

# End of file!