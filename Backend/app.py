from flask import Flask, request, Response
import os
import json
from extract_video.VideoExtractor import VideoExtractor
from build_response.ResponseBuilder import ResponseBuilder
from flask import send_file

# initialises app
app = Flask(__name__)

# sets up variables for later use
VIDEO_DIR = './video'
app.secret_key = "super secret key"
app.config["UPLOAD_FOLDER"] = VIDEO_DIR


@app.route('/')
def hello_world():
    return 'Hello User !'


# receives and stores file using for example
@app.route('/', methods=['POST'])
def process_videos():
    """
    :return: sends back results
    """
    # parses the received request
    video_file, video_name, json_file, json_name = '', '', ''
    # extracts the Video file, ending with mp4, and the json file
    # for configuration and processing the video
    for f in request.files.getlist("file"):
        if f.filename.split('.')[1] == "mp4":
            video_file = f
            video_name = video_file.filename
        elif f.filename.split('.')[1] == 'json':
            json_file = f
            json_file.save('config.json')

    # tries to read the json config file, for knowing whether to treat the video as a sample (analyse and store)
    # or as trial, (analyse, not store, and send results back)
    is_sample = False
    try:
        with open('config.json') as json_file:
            config = json.load(json_file)
        is_sample = config['is_sample']
        compare_to = config['compare_to']
    except OSError:
        is_sample = True
        compare_to = ''

    # creates necessary directory if required
    video_path = os.path.join(VIDEO_DIR, video_name)
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
    input_path = os.path.join(VIDEO_DIR, video_name)
    video_file.save(input_path)

    # sends back Added sample response, in case of adding a sample
    # sends back Analysis results, in case of trial video
    if is_sample:
        vd = VideoExtractor(media_dir="./media", model_path="../../openpose/models/")  # framerate > 1 !!!
        vd.extract(video_path, video_name.split('.')[0], framerate=30)
        return Response(status=200, response="Added sample")
    else:
        rb = ResponseBuilder(input_path=input_path,
                             sample_id=compare_to.split('.')[0])
        result_path = rb.build()
        return send_file(result_path, 'result.zip', as_attachment=True)


# starts the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
