from build_response.analyze_movement.MovementAnalyzer import MovementAnalyzer


class ResponseBuilder:
    def __init__(self, sample_id, input_path):
        self.input_path = input_path
        self.analyze = MovementAnalyzer(sample_id)
        self.data = list()

    def build(self):
        self.data = self.analyze(self.input_path)

        threshold = 10
        frame_radius = 2  # number of frames to display before and after

        index_of_failure = 0

        try:
            index_of_failure = next(i for i, val in enumerate(self.data) if val["score"] > threshold)
        except Exception:
            pass

        start = index_of_failure-frame_radius if index_of_failure > frame_radius else 0
        end = index_of_failure - frame_radius if len(self.data) > frame_radius+index_of_failure else len(self.data)-1

        vis = self.visualize(start, end)
        """
        TODO append visualization and raw_data for sending back
        """
        return self.data

    def visualize(self, start, end):
        # return visualization???
        # TODO basic loading of corresponding video frames
        # TODO 2 add scaled visualization (how to access transformation matrix in a clean way?)
        return "dummy"