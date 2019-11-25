from flask import Flask, request, Response
import os
import json

from extract_video.VideoExtractor import VideoExtractor
from build_response.ResponseBuilder import ResponseBuilder

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
    # video_file = request.files['file']
    video_file, video_name, json_file, json_name = '', '', '', ''

    for f in request.files.getlist("file"):
        if f.filename.split('.')[1] == "mp4":
            video_file = f
            video_name = video_file.filename
        elif f.filename.split('.')[1] == 'json':
            json_file = f
            json_name = json_file.filename

    is_sample = False
    config = json.load(json_file)
    is_sample = config['is_sample'] # <- boolean
    compare_to = config['compare_to'] # <-- samplevideo

    video_path = os.path.join(VIDEO_DIR, video_name)
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
    input_path = os.path.join(VIDEO_DIR, video_name)
    video_file.save(input_path)

    print(f'is_sample: {is_sample}')
    print(f'video_path: {video_path}')
    print(f'video_name: {video_name}')
    print(f'compare_to: {compare_to}')

    if is_sample:
        vd = VideoExtractor(media_dir="./media", model_path="../../openpose/models/")  # framerate > 1 !!!
        body_points = vd.extract(video_path, video_name.split('.')[0], framerate=30)
        return Response(status=200, response="Added sample")
    else:
        rb = ResponseBuilder(input_path=video_path,sample_id=video_name.split('.')[0])  # video_path: attempt, sample_id: sample
        result = rb.build()
        return Response(status=200, response="json.dumps(result)")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
