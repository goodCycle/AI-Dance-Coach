import cv2
import os
import shutil
import numpy as np

from extract_video.posewrapper.PosePredictor import PosePredictor


class VideoExtractor:

    def __init__(self, media_dir="./media", model_path="../../openpose/models/"):
        """
        :param media_dir: path to dir, where the results are stored
        :param model_path: path to used model
        """

        # check if media dir exists, build it if necessary for storing results
        self.media_dir = media_dir
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # initialise Pose Predictor and a lot of other variables :[]
        self.predictor = PosePredictor(model=model_path, disable_blending=False)
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

    # clear a directory recursively if necessary and create it
    @staticmethod
    def clear_and_create(directory):
        """
        :param directory: path to directory that could be cleared and created
        :return: void
        """
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
        os.makedirs(directory, exist_ok=True)

    def get_body_points(self):
        return self.body_points

    def extract(self, video_path, result_name, framerate):
        """
        :param video_path: the path to the video that should be extracted
        :param result_name: name of the video, used for creating a folder with the analysis results
        :param framerate: rate at which the frames from the Video should be sampled
        :return: void
        """

        # creating storing variables for later use
        self.video_path = video_path
        self.video = cv2.VideoCapture(self.video_path)
        self.frequency = 1 / framerate
        self.result_dir = os.path.join(self.media_dir, result_name)
        self.picture_dir = os.path.join(self.result_dir, "pictures")
        self.skeleton_dir = os.path.join(self.result_dir, "skeletons")
        self.body_dir = os.path.join(self.result_dir, "bodies_keypoints")

        # clear previous result with same id
        VideoExtractor.clear_and_create(self.result_dir)
        self._sample_pictures()
        self._extract_keypoints()
        self._generate_video()

        return self.body_points

    # samples the pictures from the Video and stores them in picture dir
    def _sample_pictures(self):
        """
        :return:
        """
        VideoExtractor.clear_and_create(self.picture_dir)

        # extracts a frame at a given location in the video, for reuse later
        def get_frame(sec):
            self.video.set(cv2.CAP_PROP_POS_FRAMES, sec)
            has_frames, image = self.video.read()
            if has_frames:
                cv2.imwrite(os.path.join(self.picture_dir, str(count) + ".jpg"), image)
            return has_frames

        # samples the images out of the Video, for analysing them into the pose predictor later on
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

    # extracts the key points from the images, by using Pose Predictor and stores them in the respective directory
    def _extract_keypoints(self):
        """
        :return: void
        """
        VideoExtractor.clear_and_create(self.skeleton_dir)
        VideoExtractor.clear_and_create(self.body_dir)

        # extracts the key points, as points and as overlays in the respective pictures, for reuse in
        # difference calculation and video snipped creation
        for i, pictures in enumerate(sorted(os.listdir(self.picture_dir), key=lambda x: int(x.split('.')[0]))):
            datum = self.predictor.predict_image(os.path.join(self.picture_dir, pictures))
            self.body_points.append(datum.poseKeypoints)
            np.save(os.path.join(self.body_dir, str(i) + ".npy"), datum.poseKeypoints)
            cv2.imwrite(os.path.join(self.skeleton_dir, str(i) + ".jpg"), datum.cvOutputData)

    # generates a video of the full analysed pictures
    def _generate_video(self):
        """
        :return: void
        """
        img_arr = []
        for file in sorted(os.listdir(self.skeleton_dir),
                           key=lambda x: int(x.split('.')[0])):
            img = cv2.imread(os.path.join(self.skeleton_dir, file))
            img_arr.append(img)

        shape = img_arr[0].shape[1::-1]
        out = cv2.VideoWriter(os.path.join(self.result_dir, 'skeleton_video.avi'),
                              cv2.VideoWriter_fourcc(*'DIVX'), 30, shape)
        for img in img_arr:
            out.write(img)
        out.release()
