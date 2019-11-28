import sys
import cv2
from compressType import CompressType
from image2RLE import Image2RLE
from RLE2image import RLE2Image
from cocoKeyptEval import KeypointEval

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
        ##################   Compression    ##################
        # TODO run (a part of) cocoapi pose images through openpose and evaluate accuracy
        '''
        predict_image(image_path)
        '''
        # TODO run compression across dataset
        '''
        # output_path = "compressed_image.bmp"
        compress_image(CompressType.LUM, image_path, output_path)
        '''
        # TODO run compressed images through openpose

        ######################################################

        ##################   Similarity     ##################
        # TODO: feed in ground truth json
        '''
        ground_truth = 'gt.json'
        '''
        # TODO: feed in openpose/openpose compressed json
        '''
        openpose_result = 'openpose.json'
        openpose_comp_result = 'openpose_comp.json'
        '''

        # get keypoint similarities between
        # - ground truth and openpose
        # - ground truth and openpose compressed
        # - openpose and openpose compressed
        '''
        keypoint_similarity(ground_truth, openpose_result)
        keypoint_similarity(ground_truth, openpose_comp_result)
        keypoint_similarity(openpose_result, openpose_comp_result)
        '''
        ######################################################
        
        # TODO save data for future visualization or analysis
        pass

    # parameterized image compression
    # COMP_TYPE tells "How to compress" - Luminance or Chrominance
    @staticmethod
    def compress_image(comp_type, input_img, output_img):
        enc_txt = "rle.txt"
        Image2RLE(comp_type, input_img, enc_txt)
        RLE2Image(comp_type, enc_txt, output_img)

    @staticmethod
    def keypoint_similarity(keypoints_a, keypoints_b):
        KeypointEval(keypoints_a, keypoints_b)

    def predict_image(self, image_path):
        datum = op.Datum()
        image_to_process = cv2.imread(image_path)
        datum.cvInputData = image_to_process
        self.opWrapper.emplaceAndPop([datum])

        return datum.poseKeypoints
