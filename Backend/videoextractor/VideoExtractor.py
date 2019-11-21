import cv2
import os
import shutil
import json

from posewrapper.PosePredictor import PosePredictor


class VideoExtractor:

    def __init__(self, video_name="anonymous", video_dir="./video",
                 media_dir="./media", model_path="../../openpose/models/",
                 framerate=-1):
        self.video_name = video_name
        self.video_path = os.path.join(video_dir, video_name)
        self.media_dir = media_dir
        self.picture_dir = os.path.join(self.media_dir, "pictures")
        self.skeleton_dir = os.path.join(self.media_dir, "skeletons")
        self.body_dir = os.path.join(self.media_dir, "bodies")

        self.video = cv2.VideoCapture(self.video_path)
        self.predictor = PosePredictor(model=model_path, disable_blending=True)
        self.frequency = 1 / framerate

    def __call__(self, *args, **kwargs):
        return self.extract(*args, **kwargs)

    def clear_dir(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
        os.makedirs(directory)

    def extract(self):
        self.video = cv2.VideoCapture(self.video_path)
        # clear previous media with same id
        self.clear_dir(self.media_dir)

        self._sample_pictures()
        print(2)
        self._extract_keypoints()
        print(3)
        self._overlay_images()
        print(4)
        self._generate_video()
        print(5)
        self._generate_video(use_overlayed=False)
        print(6)

    #  it will capture image in each 0.5 second
    def _sample_pictures(self):
        self.clear_dir(self.picture_dir)

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
        print(2.1)
        self.clear_dir(self.skeleton_dir)
        self.clear_dir(self.body_dir)
        for i, pictures in enumerate(os.listdir(self.picture_dir)):
            print(2.2)
            datum = self.predictor.predict_image(os.path.join(self.picture_dir, pictures))

            with open(os.path.join(self.body_dir, str(i) + ".json")) as f:
                json.dump(datum.poseKeypoints, f)
            cv2.imwrite(os.path.join(self.skeleton_dir, str(i) + ".jpg"), datum.cvOutputData)
            '''
            print("Body keypoints: \n" + str(datum.poseKeypoints))
            print("Face keypoints: \n" + str(datum.faceKeypoints))
            print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
            print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
            '''
        print(2.3)

    def _overlay_images(self):
        # https://stackoverflow.com/questions/38627870/how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white
        pass

    def _generate_video(self, use_overlayed=False):
        # Little priority
        pass
