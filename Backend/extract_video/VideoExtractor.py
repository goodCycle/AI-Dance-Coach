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
        self.overlay_dir = ""
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
        self.overlay_dir = os.path.join(self.result_dir, "overlays")

        # clear previous result with same id
        VideoExtractor.create_and_clear(self.result_dir)
        self._sample_pictures()
        self._extract_keypoints()
        self._generate_video()
        return self.body_points

    #  it will capture image in each 0.5 second
    def _sample_pictures(self):
        VideoExtractor.create_and_clear(self.picture_dir)
        '''
        def get_frame(sec):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, sec)  # (cv2.CAP_PROP_POS_MSEC, sec * 1000)
            has_frames, image = self.video.read()
            if has_frames:
                print(f'count: {count}')
                cv2.imwrite(os.path.join(self.picture_dir, str(count) + ".jpg"), image)  # save frame as JPG file
            return has_frames
        
        sec = 0
        count = 1
        success = get_frame(sec)
         count = 0
        while True:
            #count += 1
            print(f'count: {count}')
            (grabbed, frame) = self.video.read()
            if not grabbed:
                break
            else:
                cv2.imwrite(os.path.join(self.picture_dir, str(count) + ".jpg"), frame)
                count += 1
                 # sec += self.frequency
            # sec = round(sec, 2)
            # print(f"sec: {sec}")
            # success = get_frame(count)# old: (sec)
        '''
        i = 0
        k = 10
        while True:
            self.video.set(1, i)
            res, frame = self.video.read()
            if not res and k == 0:
                break
            else:
                if not res:
                    k -= 1
                    i += 1
                    continue
                print(f'i: {i}, res: {res}, k:{k}')
                cv2.imwrite(os.path.join(self.picture_dir, str(i) + ".jpg"), frame)
                i += 1

    def _extract_keypoints(self):
        # put in loop
        VideoExtractor.create_and_clear(self.skeleton_dir)
        VideoExtractor.create_and_clear(self.body_dir)

        for i, pictures in enumerate(sorted(os.listdir(self.picture_dir), key=lambda x: int(x.split('.')[0]))):
            datum = self.predictor.predict_image(os.path.join(self.picture_dir, pictures))
            self.body_points.append(datum.poseKeypoints)
            np.save(os.path.join(self.body_dir, str(i) + ".npy"), datum.poseKeypoints)
            cv2.imwrite(os.path.join(self.skeleton_dir, str(i) + ".jpg"), datum.cvOutputData)

    # currently not working :/
    def _overlay_images(self):
        VideoExtractor.create_and_clear(self.overlay_dir)
        for i, (pic, ske) in enumerate(zip(sorted(os.listdir(self.picture_dir), key=lambda x: int(x.split('.')[0])),
                                           sorted(os.listdir(self.skeleton_dir),
                                                  key=lambda x: int(x.split('.')[0])))):
            picture = Image.open(os.path.join(self.picture_dir, pic), 'r')
            skeleton = Image.open(os.path.join(self.skeleton_dir, ske), 'r')
            overlay = Image.new(mode='RGB', size=picture.size)
            overlay.paste(picture, (0, 0))
            overlay.paste(skeleton, (0, 0))
            overlay.save(os.path.join(self.overlay_dir, str(i) + ".jpg"), format="JPEG")

    def _generate_video(self):
        img_arr = []

        for file in sorted(os.listdir(self.skeleton_dir),
                           key=lambda x: int(x.split('.')[0])):
            img = cv2.imread(os.path.join(self.skeleton_dir, file))
            img_arr.append(img)

        size = img_arr[0].shape[1::-1]
        out = cv2.VideoWriter(os.path.join(self.result_dir, 'skeleton_video.avi'),
                              cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
        for img in img_arr:
            out.write(img)
        out.release()
