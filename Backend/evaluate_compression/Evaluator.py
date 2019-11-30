import sys
import cv2
import json
from .jpegDCT import ApplyDCTcomp
# from .compressType import CompressType
# from .image2RLE import Image2RLE
# from .RLE2image import RLE2Image
from .cocoKeyptEval import KeypointEval

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
        # run (a part of) cocoapi pose images through openpose and evaluate accuracy
        # image_path = 'http://farm8.staticflickr.com/7247/7813035534_1d9944d6d9_z.jpg'
        # image_path = 'C:\\Users\\avohd\\downloads\\CS470\\PoseCoach\\DancePose\\Backend\\evaluate_compression\\7813035534_1d9944d6d9_z.jpg'
        image_path = '/home/AI-Dance-Coach/Backend/evaluate_compression/7813035534_1d9944d6d9_z.jpg'
        bbox = [378.09,241.9,53.52,150.09]
        keypts = predict_image(image_path)
        
        # run compression across (a part of) dataset
        # output_path = "C:\\Users\\avohd\\downloads\\CS470\\PoseCoach\\DancePose\\Backend\\evaluate_compression\\compressed_image.jpg"
        output_path = '/home/AI-Dance-Coach/Backend/evaluate_compression/compressed_img.jpg'
        SSE = self.compress_image(40, image_path, output_path)
        print("Sum of squared error: ",SSE)
        # self.compress_image(CompressType.LUM, image_path, output_path)

        # run (a part of) compressed images through openpose
        keypts_comp = predict_image(output_path)
        ######################################################

        ##################   Similarity     ##################
        # feed in openpose/openpose compressed keypoints
        openpose_result = keypts
        openpose_comp_result = keypts_comp

        # get keypoint similarities between
        # - ground truth and openpose
        # - ground truth and openpose compressed
        # - openpose and openpose compressed
        '''
        keypoint_similarity(ground_truth, openpose_result)
        keypoint_similarity(ground_truth, openpose_comp_result)
        '''
        keypoint_similarity(bbox, openpose_result, openpose_comp_result)
        ######################################################

    # parameterized image compression with scalable quality factor QF
    # QF = [1..99]
    def compress_image(self, qf, input_path, output_path):
        return ApplyDCTcomp(qf)
    # def compress_image(self, comp_type, input_img, output_img):
        # enc_txt = "C:\\Users\\avohd\\downloads\\CS470\\PoseCoach\\DancePose\\Backend\\evaluate_compression\\rle.txt"
        # Image2RLE(comp_type, input_img, enc_txt)
        # print("compressed to rle.txt")
        # RLE2Image(comp_type, enc_txt, output_img)
        # print("compressed to bmp image")

    def keypoint_similarity(self, bbox, keypoints_a, keypoints_b):
        json_a = self.jsonify_keypts(keypoints_a, bbox)
        json_b = self.jsonify_keypts(keypoints_b, bbox)
        KeypointEval(json_a, json_b)
    
    # Reference: http://cocodataset.org/#keypoints-eval
    def jsonify_keypts(self, keypts_list, bbox):
        json_pts = {
            'keypoints': [],
            'bbox': bbox
        }

        for person in keypts_list:
            for pt in person:
                json_pts['keypoints'].append(pt[0])   # x
                json_pts['keypoints'].append(pt[1])   # y
                json_pts['keypoints'].append(2)       # v=2: labeled and visible
            
        return json.dumps(json_pts)

    def predict_image(self, image_path):
        datum = op.Datum()
        image_to_process = cv2.imread(image_path)
        datum.cvInputData = image_to_process
        self.opWrapper.emplaceAndPop([datum])

        return datum.poseKeypoints
