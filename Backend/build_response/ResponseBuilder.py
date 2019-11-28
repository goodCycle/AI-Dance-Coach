from build_response.analyze_movement.MovementAnalyzer import MovementAnalyzer
import cv2
import os
import tarfile
import shutil
from PIL import Image


def create_and_clear(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory, exist_ok=True)


class ResponseBuilder:
    def __init__(self, sample_id, input_path):
        self.input_path = input_path
        self.sample_id = sample_id
        self.analyze = MovementAnalyzer(sample_id)
        self.data = list()
        self.result_dir = './media/temp_vid'

    def build(self):
        self.data = self.analyze(self.input_path)
        print(*[(x["frame_number"], x["score"]) for x in self.data])
        threshold = 120
        frame_radius = 5  # number of frames to display before and after
        index_of_failure = 0
        try:
            index_of_failure = next(i for i, val in enumerate(self.data) if val["score"] > threshold)
        except Exception:
            pass
        start = index_of_failure - frame_radius if index_of_failure > frame_radius else 0
        # faulty
        end = index_of_failure + frame_radius if len(self.data) > frame_radius + index_of_failure else len(
            self.data) - 1

        trial_frames = list(range(start, end + 1))  # is empty
        sample_frames = [self.data[i]["frame_number"] for i in trial_frames]  # is empty

        result_dict = self.visualize(trial_frames, sample_frames)
        tar_path = os.path.join(self.result_dir, 'result.tar.gz')
        # correct until this line

        with tarfile.open(tar_path, 'w:gz')as tar:
            tar.add(result_dict['sample_result_path'])
            tar.add(result_dict['trail_result_path'])
            tar.close()
        return tar_path

    # expects 2 lists of file paths to the correct files
    def visualize(self, trial_frames, sample_frames):
        sample_dir = os.path.join("./media", self.sample_id, 'skeletons')
        trial_dir = os.path.join('./media', 'temp_vid', 'skeletons')
        sample_frames = [os.path.join(sample_dir, str(x) + '.jpg') for x in sample_frames]
        trial_frames = [os.path.join(trial_dir, str(x) + '.jpg') for x in trial_frames]

        array_trial = []
        array_sample = []
        # add path to files if necessary
        for frame_trial, frame_sample in zip(trial_frames, sample_frames):
            img_trial = cv2.imread(frame_trial)
            array_trial.append(img_trial)
            img_sample = cv2.imread(frame_sample)
            array_sample.append(img_sample)

        shape = array_trial[0].shape[1::-1]
        trial_path = os.path.join(self.result_dir, 'trial.avi')
        out_trail = cv2.VideoWriter(trial_path,
                                    cv2.VideoWriter_fourcc(*'DIVX'), 30, shape)
        for img in array_trial:
            out_trail.write(img)
        out_trail.release()
        sample_path = os.path.join(self.result_dir, 'sample.avi')
        out_sample = cv2.VideoWriter(sample_path,
                                     cv2.VideoWriter_fourcc(*'DIVX'),
                                     30, shape)
        for img in array_sample:
            out_sample.write(img)
        out_sample.release()
        return {
            'sample_path': sample_path,
            'trial_path': trial_path
        }


'''
.media/temp_vid/sample.avi
./media/temp_vid/skeleton_video.avi
'''
