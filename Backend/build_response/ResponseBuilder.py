from build_response.analyze_movement.MovementAnalyzer import MovementAnalyzer
import cv2
import os
import tarfile


class ResponseBuilder:
    def __init__(self, sample_id, input_path):
        self.input_path = input_path
        self.sample_id = sample_id
        self.analyze = MovementAnalyzer(sample_id)
        self.data = list()
        self.result_dir = '.media/result'

    def build(self):
        self.data = self.analyze(self.input_path)

        print(*[(x["frame_number"], x["score"]) for x in self.data])
        threshold = 10
        frame_radius = 2  # number of frames to display before and after
        index_of_failure = 0
        try:
            index_of_failure = next(i for i, val in enumerate(self.data) if val["score"] > threshold)
        except Exception:
            pass
        print(f'index_of_failure: {index_of_failure}')
        start = index_of_failure - frame_radius if index_of_failure > frame_radius else 0
        # faulty
        end = index_of_failure + frame_radius if len(self.data) > frame_radius + index_of_failure else len(
            self.data) - 1

        print(f'start:{start}, end: {end}')

        trial_frames = list(range(start, end + 1)) # is empty
        sample_frames = [self.data[i]["frame_number"] for i in trial_frames]# is empty

        print(f'trial_frames(1): {trial_frames}')
        print(f'sample_frames(1):{sample_frames}')


        result_dict = self.visualize(trial_frames, sample_frames)
        tar_path = os.path.join(self.result_dir, 'result.tar.gz')
        tar = tarfile.open(tar_path, 'w:gz')
        # add json in required
        tar.add(result_dict['sample_result_path'])
        tar.add(result_dict['trail_result_path'])
        tar.close()
        return tar_path

    # expects 2 lists of file paths to the correct files
    def visualize(self, trial_frames, sample_frames):
        # todo: build file paths
        sample_dir = os.path.join("./media", self.sample_id, 'skeletons')
        trial_dir = os.path.join('./media', 'temp_vid', 'skeletons')
        print(f'sample_dir:{sample_dir}, len(sample_frames): {sample_frames}')
        print(f'trial_dir: {trial_dir}, len(trial_frames): {trial_frames}')

        sample_frames = [os.path.join(sample_dir, x, '.jpg') for x in sample_frames]
        trial_frames = [os.path.join(trial_dir, x, '.jpg') for x in trial_frames]

        print(f'sample_frames[0]: {sample_frames[0]}')
        print(f'trial_frames[0]: {trial_frames[0]}')

        array_trail = []
        array_sample = []
        # add path to files if necessary
        for file_trial, file_sample in zip(trial_frames, sample_frames):
            picture_trail = cv2.imread(file_trial, 'r')
            array_trail.append(picture_trail)
            picture_sample = cv2.imread(file_sample, 'r')
            array_sample.append(picture_sample)

        print(f'len(array_trail): {len(array_trail)}')
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
        return {'sample_result_path': sample_result_path,
                'trail_result_path': trail_result_path
                }
