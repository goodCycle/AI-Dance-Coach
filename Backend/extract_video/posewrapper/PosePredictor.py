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

    def __init__(self, model="../../openpose/models/", disable_blending =False):  # "../../../openpose/models/"?

        params = dict()
        params["model_folder"] = model

        params["model_pose"] = "BODY_25"

        # TODO set as parameter (transmit from the device?)
        params["net_resolution"] = "-1x368"
        params["disable_blending"] = str(disable_blending)  # check if broken
        # params["scale_number"] = "4"
        # params["scale_gap"] = "0.25"

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

    def predict_image(self, image_path):
        datum = op.Datum()
        image_to_process = cv2.imread(image_path)
        datum.cvInputData = image_to_process
        self.opWrapper.emplaceAndPop([datum])

        # Display Image


        return datum

    # TODO implement multi-picture inference
