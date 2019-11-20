import cv2
import os
import shutil

from posewrapper.PosePredictor import PosePredictor


class VideoExtractor:

    def __init__(self):
        self.video_id = ""
        self.src_path = ""
        self.frequency = 0

        self.video = cv2.VideoCapture(self.src_path)
        self.media_dir = os.path.join(self.MEDIA_ROOT, str(id))

        self.predictor = PosePredictor(model="../../openpose/models/", disable_blending=True)
        self.MEDIA_ROOT = "./media"

    def __call__(self, *args, **kwargs):
        return self.extract(*args, **kwargs)

    def extract(self, video_id, src_path, framerate):

        self.video_id = video_id
        self.src_path = src_path
        self.frequency = 1 / framerate

        self.video = cv2.VideoCapture(self.src_path)
        self.media_dir = os.path.join(self.MEDIA_ROOT, str(id))

        if not os.path.exists(self.MEDIA_ROOT):
            os.makedirs(self.MEDIA_ROOT)

        # clear previous media with same id
        if os.path.exists(self.media_dir):
            shutil.rmtree(self.media_dir, ignore_errors=True)

        os.makedirs(self.media_dir)

        self._sample_pictures()
        self._extract_keypoints()
        self._overlay_images()

        self._generate_video()
        self._generate_video(use_overlayed=False)

    #  it will capture image in each 0.5 second
    def _sample_pictures(self):

        def get_frame(sec):
            self.video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
            has_frames, image = self.video.read()
            if has_frames:
                cv2.imwrite("./images/" + str(count) + ".jpg", image)  # save frame as JPG file
            return has_frames

        sec = 0
        count = 1
        success = get_frame(sec)

        while success:
            count += 1
            sec += self.frequency
            sec = round(sec, 2)
            success = get_frame(sec)

    def _extract_keypoints(self):

        # put in loop
        datum = self.predictor.predict_image('images/1.jpg')

        print("Body keypoints: \n" + str(datum.poseKeypoints))
        print("Face keypoints: \n" + str(datum.faceKeypoints))
        print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
        print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))

        cv2.imwrite("test.jpg", datum.cvOutputData)  # skeleton - Black background


        pass

    def _overlay_images(self):
        # https://stackoverflow.com/questions/38627870/how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white
        pass

    def _generate_video(self, use_overlayed=False):
        # Little priority
        pass

