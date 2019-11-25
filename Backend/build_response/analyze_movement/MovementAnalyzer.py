from extract_video.VideoExtractor import VideoExtractor
from build_response.analyze_movement.pose_difference.DifferenceCalculator import DifferenceCalculator


class MovementAnalyzer:

    def __init__(self, sample_id):
        self.extract = VideoExtractor(media_dir="./media", model_path="../../openpose/models/")
        self.difference = DifferenceCalculator(sample_keypoint_path="./media/"+sample_id+"/bodies_keypoints")

    def __call__(self, *args, **kwargs):
        return self.analyze(*args, **kwargs)

    def analyze(self, input_path):

        analyzation_fps = 15
        sample_fps = 30

        step = sample_fps/analyzation_fps
        poses = self.extract.extract(input_path, "temp_vid", analyzation_fps)

        score_dicts = self.difference([(pose, i*step) for i, pose in enumerate(poses)])

        result = list()
        for i, score_dict in enumerate(score_dicts):

            current_frame_dict = dict()
            current_frame_dict["frame_number"] = i*step
            current_frame_dict["score"] = sum([score*weight for _, (score, weight) in score_dict.items()])
            current_frame_dict["raw_data"] = score_dict

            result.append(current_frame_dict)

        return result

