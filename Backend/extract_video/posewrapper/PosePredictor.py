import sys
import cv2
import os

try:
    sys.path.append('/usr/local/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found.')
    raise e


class PosePredictor:
    """
    A wrapper that initializes the internal OpenPose Wrapper and
    exposes a method to extract pose keypoints from singular images.
    """

    def __init__(self, model="../../openpose/models/", disable_blending =False):

        # Flags for calling OpenPose
        params = dict()
        params["model_folder"] = model
        params["model_pose"] = "BODY_25"
        params["net_resolution"] = "-1x368"
        params["disable_blending"] = str(disable_blending)

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

    def predict_image(self, image_path):
        """

        :param image_path: the file path to the image to be analyzed
        :return: The result of the inference by OpenPose
        """
        datum = op.Datum()
        image_to_process = cv2.imread(image_path)
        datum.cvInputData = image_to_process
        self.opWrapper.emplaceAndPop([datum])
        return datum
