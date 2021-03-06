from extract_video.VideoExtractor import VideoExtractor
from build_response.analyze_movement.pose_difference.DifferenceCalculator import DifferenceCalculator


class MovementAnalyzer:
    """
    Handles the video extraction and pose comparison to provide data that aids
    the locating of the first mistake in the performance videos
    """

    def __init__(self, sample_id):
        self.extract = VideoExtractor(media_dir="./media", model_path="../../openpose/models/")
        self.difference = DifferenceCalculator(sample_keypoint_path="./media/" + sample_id + "/bodies_keypoints")

    def __call__(self, *args, **kwargs):
        return self.analyze(*args, **kwargs)

    def analyze(self, input_path):
        analyzation_fps = 30
        sample_fps = 30

        step = sample_fps / analyzation_fps
        poses = self.extract(input_path, "temp_vid", analyzation_fps)

        score_dicts = self.difference([(pose, int(i * step)) for i, pose in enumerate(poses)])

        # Builds the result data structure:
        # List of dicts, one for each input frame:
        #   frame_number: frame number of the corresponding frame in the sample video
        #   score: weighted score for pose difference
        #   raw_data: the raw dictionary created by DifferenceCalculator
        result = list()
        for i, (score_dict, frame_num) in enumerate(score_dicts):
            current_frame_dict = dict()
            current_frame_dict["frame_number"] = frame_num
            current_frame_dict["score"] = sum([int(score * weight * 1000) for _, (score, weight) in score_dict.items()])
            current_frame_dict["raw_data"] = score_dict

            result.append(current_frame_dict)
        return result
