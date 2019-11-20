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

    def __init__(self, model="../../openpose/models/"):  # "../../../openpose/models/"?

        params = dict()
        params["model_folder"] = model

        params["model_pose"] = "BODY_25"  # "BODY_25B"D

        # TODO set as parameter (transmit from the device?)
        params["net_resolution"] = "-1x368"
        params["disable_blending"] = "True"
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
        print("Body keypoints: \n" + str(datum.poseKeypoints))
        print("Face keypoints: \n" + str(datum.faceKeypoints))
        print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
        print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))

        cv2.imwrite("test.jpg", datum.cvOutputData)

        return datum

    # TODO implement multi-picture inference
