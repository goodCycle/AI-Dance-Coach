import cv2
import os
import shutil
import json
import codecs
from PIL import Image

from posewrapper.PosePredictor import PosePredictor

'''
    media
    -> 0
        -> video
        -> skeleton
        -> ...
    -> 1
        -> video
        -> skeleton
        -> ...
'''


class VideoExtractor:

    def __init__(self, video_name="anonymous", video_dir="./video",
                 media_dir="./media", model_path="../../openpose/models/",
                 framerate=-1):
        self.video_name = video_name
        self.video_path = os.path.join(video_dir, video_name)

        self.media_dir = media_dir
        self.picture_dir = os.path.join(self.media_dir, "pictures")
        self.skeleton_dir = os.path.join(self.media_dir, "skeletons")
        self.body_keypoints_dir = os.path.join(self.media_dir, "bodies_keypoints")
        self.overlay_dir = os.path.join(self.media_dir, "overlays")

        self.video = cv2.VideoCapture(self.video_path)
        self.predictor = PosePredictor(model=model_path, disable_blending=True)
        self.frequency = 1 / framerate

    def __call__(self, *args, **kwargs):
        return self.extract(*args, **kwargs)

    def clear_and_create(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
        os.makedirs(directory)

    def extract(self):
        self.video = cv2.VideoCapture(self.video_path)
        # clear previous media with same id
        self.clear_and_create(self.media_dir)

        self._sample_pictures()
        self._extract_keypoints()
        self._overlay_images()
        self._generate_video()
        self._generate_video(use_overlayed=False)

    #  it will capture image in each 0.5 second
    def _sample_pictures(self):
        self.clear_and_create(self.picture_dir)

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
        self.clear_and_create(self.skeleton_dir)
        self.clear_and_create(self.body_keypoints_dir)
        for i, pictures in enumerate(os.listdir(self.picture_dir)):
            datum = self.predictor.predict_image(os.path.join(self.picture_dir, pictures))
            datum_list = datum.poseKeypoints.tolist()
            json.dump(datum_list,
                      codecs.open(os.path.join(self.body_keypoints_dir, str(i) + ".json"), 'w', encoding='utf-8'),
                      separators=(',', ':'))  ### this saves the array in .json format
            cv2.imwrite(os.path.join(self.skeleton_dir, str(i) + ".jpg"), datum.cvOutputData)

    def _overlay_images(self):
        self.clear_and_create(self.overlay_dir)
        for i, (pic, ske) in enumerate(zip(os.listdir(self.picture_dir), os.listdir(self.skeleton_dir))):
            picture = Image.open(os.path.join(self.picture_dir, pic), 'r').convert("RGBA")
            skeleton = Image.open(os.path.join(self.skeleton_dir, ske), 'r').convert("RGBA")
            text_img = Image.new('RGBA', picture.size, (0, 0, 0, 0))
            text_img.paste(picture, (0, 0))
            text_img.paste(skeleton, (0, 0), mask=skeleton)
            text_img = text_img.convert("RGB")
            text_img.save(os.path.join(self.overlay_dir, str(i) + ".jpg"), format="JPEG")
        # https://stackoverflow.com/questions/38627870/how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white

    def _generate_video(self, use_overlayed=False):
        img_arr = []
        for file in os.listdir(self.overlay_dir):
            img = cv2.imread(os.path.join(self.overlay_dir, file))
            img_arr.append(img)

        size = img_arr[0].shape[1::-1]

        out = cv2.VideoWriter(os.path.join(self.media_dir, 'overlay_video.avi'),
                              cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
        for img in img_arr:
            out.write(img)
        out.release()
        # https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
        # to find out, how to build mp4 ?
