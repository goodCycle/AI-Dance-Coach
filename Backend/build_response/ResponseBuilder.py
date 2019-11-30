from build_response.analyze_movement.MovementAnalyzer import MovementAnalyzer
import cv2
import os
import shutil
import json
import zipfile


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
        frame_radius = 15  # number of frames to display before and after
        index_of_failure = 0
        successful = False
        try:
            index_of_failure = next(i for i, val in enumerate(self.data) if val["score"] > threshold)
            start = index_of_failure - frame_radius if index_of_failure > frame_radius else 0
            end = index_of_failure + frame_radius if len(self.data) > frame_radius + index_of_failure else len(
                self.data) - 1
        except Exception:
            successful = True
            start = 0
            end = len(self.data)-1

        trial_frames = list(range(start, end + 1))  # is empty
        sample_frames = [self.data[i]["frame_number"] for i in trial_frames]  # is empty
        result_dict = self.visualize(trial_frames, sample_frames)
        zip_path = os.path.join(self.result_dir, 'result.zip')

        # add json
        json_path = os.path.join(self.result_dir, 'trial.json')
        with open(json_path, 'w') as f:
            json.dump(self.data, f)

        result = {
            'success': successful,
            'fail_frame': index_of_failure
        }
        json_result_path = os.path.join(self.result_dir, 'result.json')
        with open(json_result_path, 'w') as f:
            json.dump(result, f)

        with zipfile.ZipFile(zip_path, 'w') as myzip:
            myzip.write(result_dict['sample_path'])
            myzip.write(result_dict['trial_path'])
            myzip.write(json_path)
            myzip.write(json_result_path)
            myzip.close()

        return zip_path

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
        trial_path = os.path.join(self.result_dir, 'trial.mp4')
        out_trail = cv2.VideoWriter(trial_path,
                                    cv2.VideoWriter_fourcc(*'mp4v'), 30, shape)
        for img in array_trial:
            out_trail.write(img)
        out_trail.release()
        sample_path = os.path.join(self.result_dir, 'sample.mp4')
        out_sample = cv2.VideoWriter(sample_path,
                                     cv2.VideoWriter_fourcc(*'mp4v'),
                                     30, shape)
        for img in array_sample:
            out_sample.write(img)
        out_sample.release()
        return {
            'sample_path': sample_path,
            'trial_path': trial_path
        }
