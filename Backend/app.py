from flask import Flask, request, Response
import os
import cv2
import json

from videoextractor.VideoExtractor import VideoExtractor

# simon.zocholl@mnet-mail.de

app = Flask(__name__)
UPLOAD_FOLDER = './video'

app.secret_key = "super secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# pred.predict_image(image_path) for inference

@app.route('/')
def hello_world():
    return 'Hello World!'


# receives and stores file using for example
# curl -X POST -F file=@"/mnt/c/Users/nomis/Desktop/testvideo1.mp4" http://127.0.0.1:5000
@app.route('/', methods=['POST'])
def video_in():
    video_name = "video1.mp4"
    video_dir = "./video"

    file = request.files['file']
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
    file.save(input_path)

    vd = VideoExtractor(video_name=video_name, video_dir=video_dir,
                        media_dir="./media",
                        model_path="../../openpose/models/",
                        framerate=10)
    vd.extract()
    response = Response(status=200, response="result_string")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
