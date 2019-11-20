from flask import Flask, request, Response
import os
import cv2

from posewrapper.PosePredictor import PosePredictor

app = Flask(__name__)
UPLOAD_FOLDER = './video'
IMAGE_FOLDER = './images'

app.secret_key = "super secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

pred = PosePredictor()


# call pred.predict_image(image_path) for inference

@app.route('/')
def hello_world():
    return 'Hello World!'


# receives and stores file using for example
# curl -X POST -F file=@"/mnt/c/Users/nomis/Desktop/testvideo1.mp4" http://127.0.0.1:5000
@app.route('/', methods=['POST'])
def video_in():
    file = request.files['file']
    # file_name = secure_filename(file.filename)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input_file.mp4'))

    # just for testing
    sample_pictures()
    data = '{ "Hello":"Frontend"}'
    response = Response(status=200, response=data)
    return response


#  it will capture image in each 0.5 second
def sample_pictures(frame_rate=.5):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_file.mp4')
    video = cv2.VideoCapture(video_path)

    if not os.path.exists('./images'):
        os.makedirs('./images')
    # clear previous images
    list(map(os.unlink, (os.path.join(IMAGE_FOLDER + "/", f) for f in os.listdir("images"))))

    def get_frame(sec):
        video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        has_frames, image = video.read()
        if has_frames:
            cv2.imwrite("./images/" + str(count) + ".jpg", image)  # save frame as JPG file
        return has_frames

    sec = 0
    count = 1
    success = get_frame(sec)

    while success:
        count += 1
        sec += frame_rate
        sec = round(sec, 2)
        success = get_frame(sec)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
