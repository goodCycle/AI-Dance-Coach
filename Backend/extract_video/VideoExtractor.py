import cv2
import os
import shutil
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
        self.overlay_dir = ""
        self.result_dir = ""
        self.body_points = []

    def __call__(self, *args, **kwargs):
        return self.extract(*args, **kwargs)

    @staticmethod
    def create_and_clear(directory):
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
        os.makedirs(directory)

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
        self.body_dir = os.path.join(self.result_dir, "body_keypoints")
        self.overlay_dir = os.path.join(self.result_dir, "overlays")

        # clear previous result with same id
        VideoExtractor.create_and_clear(self.result_dir)
        self._sample_pictures()
        self._extract_keypoints()
        # self._overlay_images()
        self._generate_video()
        self._generate_video(use_overlayed=False)
        return self.body_points

    #  it will capture image in each 0.5 second
    def _sample_pictures(self):
        VideoExtractor.create_and_clear(self.picture_dir)

        def get_frame(sec):
            self.video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
            has_frames, image = self.video.read()
            if has_frames:
                cv2.imwrite(os.path.join(self.picture_dir, str(count) + ".jpg"), image)  # save frame as JPG file
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
        VideoExtractor.create_and_clear(self.skeleton_dir)
        VideoExtractor.create_and_clear(self.body_dir)
        for i, pictures in enumerate(os.listdir(self.picture_dir)):
            datum = self.predictor.predict_image(os.path.join(self.picture_dir, pictures))
            np.save(os.path.join(self.body_dir, str(i) + ".npy"), datum.poseKeypoints)
            '''
            self.body_points.append(datum.poseKeypoints)  # <- store unprocessed points for return value
            datum_list = datum.poseKeypoints.tolist()
            json.dump(datum_list, codecs.open(os.path.join(self.body_dir, str(i) + ".json"), 'w', encoding='utf-8'),
                      separators=(',', ':'))  ### this saves the array in .json format
            '''
            cv2.imwrite(os.path.join(self.skeleton_dir, str(i) + ".jpg"), datum.cvOutputData)

    # currently not working :/
    def _overlay_images(self):
        VideoExtractor.create_and_clear(self.overlay_dir)
        for i, (pic, ske) in enumerate(zip(os.listdir(self.picture_dir), os.listdir(self.skeleton_dir))):
            picture = Image.open(os.path.join(self.picture_dir, pic), 'r')
            skeleton = Image.open(os.path.join(self.skeleton_dir, ske), 'r')
            overlay = Image.new(mode='RGB', size=picture.size)
            overlay.paste(picture, (0, 0))
            overlay.paste(skeleton, (0, 0))
            overlay.save(os.path.join(self.overlay_dir, str(i) + ".jpg"), format="JPEG")

    def _generate_video(self, use_overlayed=False):
        img_arr = []

        for file in os.listdir(self.skeleton_dir):
            img = cv2.imread(os.path.join(self.skeleton_dir, file))
            img_arr.append(img)

        size = img_arr[0].shape[1::-1]

        out = cv2.VideoWriter(os.path.join(self.result_dir, 'skeleton_video.avi'),
                              cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
        for img in img_arr:
            out.write(img)
        out.release()
