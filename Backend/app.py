from flask import Flask, request, Response
import os
import cv2
import json

# from extract_video.VideoExtractor import VideoExtractor

# simon.zocholl@mnet-mail.de

app = Flask(__name__)
VIDEO_DIR = './video'

app.secret_key = "super secret key"
app.config["UPLOAD_FOLDER"] = VIDEO_DIR


# pred.predict_image(image_path) for inference

@app.route('/')
def hello_world():
    return 'Hello World!'


# receives and stores file using for example
# curl -X POST -F file=@"/mnt/c/Users/nomis/Desktop/testvideo1.mp4" http://127.0.0.1:5000
@app.route('/', methods=['POST'])
def video_in():
    file = request.files['file']
    video_name = file.filename
    video_path = os.path.join(VIDEO_DIR, video_name)

    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    input_path = os.path.join(VIDEO_DIR, video_name)
    file.save(input_path)

    # vd = VideoExtractor(media_dir="./media", model_path="../../openpose/models/")  # framerate > 1 !!!
    # body_points = vd.extract(video_path, video_name.split('.')[0], framerate=30)

    response = Response(status=200, response="result_string")
    return response


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')
