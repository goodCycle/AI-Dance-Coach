import sys
import cv2

try:
    sys.path.append('/usr/local/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found.')
    raise e


class Evaluator:

    def __init__(self):
        params = dict()
        params["model_folder"] = "../../openpose/models/"

        params["model_pose"] = "BODY_25"

        params["net_resolution"] = "-1x368"  # Maybe we will need to adjust this?
        params["disable_blending"] = True
        # params["scale_number"] = "4"
        # params["scale_gap"] = "0.25"

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

        # TODO Load in coco data set

    def __call__(self, *args, **kwargs):
        return self.evaluate(*args, **kwargs)

    def evaluate(self):
        # TODO run (a part of) cocoapi pose images through openpose and evaluate accuracy
        #  predict_image(image_path)
        # TODO run compression across dataset
        # TODO run compressed images through openpose

        # TODO get keypoint similarities between
        # - ground truth and openpose
        # - ground truth and openpose compressed
        # - openpose and openpose compressed

        # TODO save data for future visualization or analysis
        pass

    @staticmethod
    def compress_image(image):
        # TODO implement some form of parameterized image compression ("How much to compress")
        pass

    @staticmethod
    def keypoint_similarity(keypoint_a, keypoints_b):
        # TODO implement OKS
        return 1

    def predict_image(self, image_path):
        datum = op.Datum()
        image_to_process = cv2.imread(image_path)
        datum.cvInputData = image_to_process
        self.opWrapper.emplaceAndPop([datum])

        return datum.poseKeypoints
