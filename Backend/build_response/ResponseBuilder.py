from build_response.analyze_movement.MovementAnalyzer import MovementAnalyzer


# TODO 2 add scaled visualization (how to access transformation matrix in a clean way?)
class ResponseBuilder:
    def __init__(self, sample_id, input_path):
        self.input_path = input_path
        self.analyze = MovementAnalyzer(sample_id)

    def build(self):
        data = self.analyze(self.input_path)

        """
        TODO add response building
        """
        return data
