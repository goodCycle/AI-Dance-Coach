import cv2
import os
import shutil
import json
import codecs
from PIL import Image
import numpy as np

from extract_video.posewrapper.PosePredictor import PosePredictor


class VideoExtractor:

    def __init__(self, media_dir="./media", model_path="../../openpose/models/"):

        self.media_dir = media_dir
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        self.predictor = PosePredictor(model=model_path, disable_blending=True)
        self.video = None
        self.frequency = -1
        self.video_path = ""
        self.picture_dir = ""
        self.skeleton_dir = ""
        self.body_dir = ""
        self.result_dir = ""
        self.body_points = []

    def __call__(self, *args, **kwargs):
        return self.extract(*args, **kwargs)

    @staticmethod
    def create_and_clear(directory):
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
        os.makedirs(directory, exist_ok=True)

    def get_body_points(self):
        return self.body_points

    # set video_path and frame rate
    def extract(self, video_path, result_name, framerate):
        self.video_path = video_path

        self.video = cv2.VideoCapture(self.video_path)
        self.frequency = 1 / framerate

        self.result_dir = os.path.join(self.media_dir, result_name)
        self.picture_dir = os.path.join(self.result_dir, "pictures")
        self.skeleton_dir = os.path.join(self.result_dir, "skeletons")
        self.body_dir = os.path.join(self.result_dir, "bodies_keypoints")

        # clear previous result with same id
        VideoExtractor.create_and_clear(self.result_dir)
        self._sample_pictures()
        self._extract_keypoints()
        self._generate_video()
        return self.body_points

    def _sample_pictures(self):
        VideoExtractor.create_and_clear(self.picture_dir)

        print(int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)))

        def get_frame(sec):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, sec)  # (cv2.CAP_PROP_POS_MSEC, sec * 1000)
            has_frames, image = self.video.read()
            if has_frames:
                cv2.imwrite(os.path.join(self.picture_dir, str(count) + ".jpg"), image)
            return has_frames

        sec = 0
        count = 0
        while count <= int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)):
            (grabbed, frame) = self.video.read()
            if not grabbed:
                count += 1
                continue
            else:
                cv2.imwrite(os.path.join(self.picture_dir, str(count) + ".jpg"), frame)
                count += 1
                sec += self.frequency
            sec = round(sec, 2)

    def _extract_keypoints(self):
        VideoExtractor.create_and_clear(self.skeleton_dir)
        VideoExtractor.create_and_clear(self.body_dir)

        for i, pictures in enumerate(sorted(os.listdir(self.picture_dir), key=lambda x: int(x.split('.')[0]))):
            datum = self.predictor.predict_image(os.path.join(self.picture_dir, pictures))
            self.body_points.append(datum.poseKeypoints)
            np.save(os.path.join(self.body_dir, str(i) + ".npy"), datum.poseKeypoints)
            cv2.imwrite(os.path.join(self.skeleton_dir, str(i) + ".jpg"), datum.cvOutputData)

    def _generate_video(self):
        img_arr = []
        for file in sorted(os.listdir(self.skeleton_dir),
                           key=lambda x: int(x.split('.')[0])):
            print(f'vidExtract: path_imgs: {os.path.join(self.skeleton_dir, file)}')
            img = cv2.imread(os.path.join(self.skeleton_dir, file))
            img_arr.append(img)

        shape = img_arr[0].shape[1::-1]
        print(f'vidExtract: path_vid: {os.path.join(self.result_dir, "skeleton_video.avi")}')
        out = cv2.VideoWriter(os.path.join(self.result_dir, 'skeleton_video.avi'),
                              cv2.VideoWriter_fourcc(*'DIVX'), 30, shape)
        for img in img_arr:
            out.write(img)
        out.release()
