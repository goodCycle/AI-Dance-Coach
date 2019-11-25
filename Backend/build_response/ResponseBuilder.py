from build_response.analyze_movement.MovementAnalyzer import MovementAnalyzer


class ResponseBuilder:
    def __init__(self, sample_id, input_path, sample_name, input_name):
        self.input_path = input_path
        self.analyze = MovementAnalyzer(sample_id)
        self.data = list()
        self.sample_name = sample_name
        self.input_name = input_name

    def build(self):
        self.data = self.analyze(self.input_path)

        threshold = 10
        frame_radius = 2  # number of frames to display before and after

        index_of_failure = 0

        try:
            index_of_failure = next(i for i, val in enumerate(self.data) if val["score"] > threshold)
        except Exception:
            print("Threshold was not reached")
            # TODO what to do if video never misses the threshold?

        start = index_of_failure-frame_radius if index_of_failure > frame_radius else 0
        end = index_of_failure - frame_radius if len(self.data) > frame_radius+index_of_failure else len(self.data)-1

        trial_frames = list(range(start, end+1))
        sample_frames = [self.data[i]["frame_number"] for i in trial_frames]

        return self.visualize(trial_frames, sample_frames)

    def visualize(self, trial_frames, sample_frames):
        sample_render_path = ""
        trial_render_path = ""
        # for the media folder self.sample_name
        #                      self.input_name

        return sample_render_path, trial_render_path
