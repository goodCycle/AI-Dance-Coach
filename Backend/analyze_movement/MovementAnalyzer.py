from videoextractor.VideoExtractor import VideoExtractor
from analyze_movement.pose_difference.DifferenceCalculator import DifferenceCalculator


class MovementAnalyzer:

    def __init__(self):
        # TODO add missing parameters
        self.extract = VideoExtractor()
        self.difference = DifferenceCalculator(sample_keypoint_path="media/bodies")

    def __call__(self, *args, **kwargs):
        return self.analyze(*args, **kwargs)

    def analyze(self, sample_id, input_path):

        analyzation_fps = 15
        sample_fps = 30

        step = sample_fps/analyzation_fps

        # TODO add missing parameters
        poses = self.extract()

        score_dicts = self.difference([(pose, i*step) for i, pose in enumerate(poses)])

        # TODO get scores per frame
        # TODO decide on what to return

        return

