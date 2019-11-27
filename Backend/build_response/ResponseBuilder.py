from build_response.analyze_movement.MovementAnalyzer import MovementAnalyzer
import cv2
import os
import tarfile


class ResponseBuilder:
    def __init__(self, sample_id, input_path):
        self.input_path = input_path
        self.analyze = MovementAnalyzer(sample_id)
        self.data = list()
        self.result_dir = '.media/result'

    def build(self):
        self.data = self.analyze(self.input_path)
        threshold = 10
        frame_radius = 2  # number of frames to display before and after
        index_of_failure = 0

        try:
            index_of_failure = next(i for i, val in enumerate(self.data) if val["score"] > threshold)
        except Exception:
            pass

        start = index_of_failure - frame_radius if index_of_failure > frame_radius else 0
        end = index_of_failure - frame_radius if len(self.data) > frame_radius + index_of_failure else len(
            self.data) - 1
        result_dict = self.visualize(start, end)
        tar_path = os.path.join(self.result_dir, 'result.tar.gz')
        tar = tarfile.open(tar_path, 'w:gz')
        # add json in required
        tar.add(result_dict['sample_result_path'])
        tar.add(result_dict['trail_result_path'])
        tar.close()
        """
        TODO append visualization and raw_data for sending back
        """
        return tar_path

    # expects 2 lists of file paths to the correct files
    def visualize(self, frames_trail, frames_sample):
        array_trail = []
        array_sample = []
        # add path to files if necessary
        for i, (file_trail, file_sample) in enumerate(zip(frames_trail, frames_sample)):
            picture_trail = cv2.imread(file_trail, 'r')
            array_trail.append(picture_trail)
            picture_sample = cv2.imread(file_sample, 'r')
            array_sample.append(picture_sample)

        size = array_trail[0].shape[1::-1]

        # where to store the files?
        trail_result_path = os.path.join(self.result_dir, 'trail.avi')
        out_trail = cv2.VideoWriter(trail_result_path,
                                    cv2.VideoWriter_fourcc(*'DIVX'),
                                    fps=30, frame_size=size)
        map(out_trail.write, array_trail)
        out_trail.release()
        sample_result_path = os.path.join(self.result_dir, 'sample.avi')
        out_sample = cv2.VideoWriter(sample_result_path,
                                     cv2.VideoWriter_fourcc(*'DIVX'),
                                     fps=30, frame_size=size)
        map(out_trail.write, array_sample)
        out_sample.release()

        # return visualization???
        # TODO basic loading of corresponding video frames
        # TODO 2 add scaled visualization (how to access transformation matrix in a clean way?)
        return {'sample_result_path': sample_result_path,
                'trail_result_path': trail_result_path
                }
