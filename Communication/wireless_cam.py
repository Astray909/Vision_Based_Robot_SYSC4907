from picamera import PiCamera
from flask import Flask, Response
import cv2

app = Flask(__name__)
camera = PiCamera()

@app.route('/')
def index():
    return "Hello, world!"

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    camera.start_recording('/dev/null', format='h264')
    app.run(host='0.0.0.0', port=5000, threaded=True)