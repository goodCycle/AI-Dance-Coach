import sys
import cv2
import json
from .jpegDCT import ApplyDCTcomp
from .avgDistance import AvgDistance

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

    def __call__(self, *args, **kwargs):
        return self.evaluate(*args, **kwargs)

    def evaluate(self, qf):
        ##################   Compression    ##################
        # run (a part of) cocoapi pose images through openpose and evaluate accuracy
        res_file = open('evaluate_results_qf%d.txt' % qf, "w")
        image_dir = '/home/pose/AI-Dance-Coach/Backend/evaluate_compression/eval-images/'
        out_suffix = '_comp{}'.format(qf)
        for pose_size in ['Large', 'Medium']:
            for img in range(10):
                image_path = "{}{}/{}.jpg".format(image_dir, pose_size, img)
                keypts = self.predict_image(image_path)
        
                # run compression across (a part of) dataset, with quality factor QF
                output_path = "{}{}{}/{}.jpg".format(image_dir, pose_size, out_suffix, img)
                self.compress_image(qf, image_path, output_path)

                # run (a part of) compressed images through openpose
                keypts_comp = self.predict_image(output_path)
        ######################################################

        ##################   Similarity     ##################
                # feed in openpose/openpose compressed keypoints
                openpose_result = keypts
                openpose_comp_result = keypts_comp

                # get keypoint similarities between openpose and openpose compressed
                # similarity is measured by 2D Euclidean distance
                similarity = AvgDistance(openpose_result, openpose_comp_result)
                res_file.write('{}{} {}\n'.format(pose_size, img, similarity.calculate()))
        res_file.close()
        ######################################################

    # parameterized image compression with scalable quality factor QF
    # QF = [1..99]
    def compress_image(self, qf, input_path, output_path):
        ApplyDCTcomp(qf, input_path, output_path)

    # Helper function that measures Object Keypoint Similarity(OKS)
    def keypoint_similarity(self, bbox, keypoints_a, keypoints_b):
        json_a = "keypoints_a_10.json"
        self.jsonify_keypts(keypoints_a, bbox, json_a)
        json_b = "keypoints_b_10.json"
        self.jsonify_keypts(keypoints_b, bbox, json_b)
        #KeypointEval(json_a, json_b)
    
    # Helper function that turns a python list of points into json file format
    # Reference: http://cocodataset.org/#keypoints-eval
    def jsonify_keypts(self, keypts_list, bbox, json_path):
        json_pts = {
            'keypoints': [],
            'bbox': bbox
        } 

        for person in keypts_list:
            for pt in person:
                json_pts['keypoints'].append(str(pt[0]))   # x
                json_pts['keypoints'].append(str(pt[1]))   # y
                json_pts['keypoints'].append(str(2))       # v=2: labeled and visible
            
        data = json.dumps(json_pts)
        with open(json_path, "w") as f:
            f.write(data)

        f.close()

    # Predicts pose based on Openpose and return estimated pose keypoints
    def predict_image(self, image_path):
        datum = op.Datum()
        image_to_process = cv2.imread(image_path)
        datum.cvInputData = image_to_process
        self.opWrapper.emplaceAndPop([datum])

        return datum.poseKeypoints
