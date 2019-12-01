from build_response.analyze_movement.MovementAnalyzer import MovementAnalyzer
import cv2
import os
import shutil
import json
import zipfile


def clear_and_create(directory):
    """
    :param directory: the directory that should be firstly cleared (recursively) and created
    :return: void
    """
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory, exist_ok=True)


# Builds the Response for comparing a trial video against a sample video
class ResponseBuilder:
    def __init__(self, sample_id, input_path):
        """
        :param sample_id: the name of the sample video
        :param input_path: the path to the sample video
        """
        self.input_path = input_path
        self.sample_id = sample_id
        self.analyze = MovementAnalyzer(sample_id)
        self.data = list()
        self.result_dir = './media/temp_vid'

    def build(self):
        """
        :return: returns the location of a zip folder, that contains the accumulated results
        """
        self.data = self.analyze(self.input_path)
        print(*[(x["frame_number"], x["score"]) for x in self.data])
        threshold = 120  # unacceptable error threshold
        frame_radius = 15  # number of frames to display before and after
        index_of_failure = 0  # index of first image with unacceptable error
        successful = False  # stores if the attempt contained an unacceptable error, gets set to TRUE of not

        # checks data for values exceeding the acceptable error threshold, sets variables appropriately
        try:
            index_of_failure = next(i for i, val in enumerate(self.data) if val["score"] > threshold)
            start = index_of_failure - frame_radius if index_of_failure > frame_radius else 0
            end = index_of_failure + frame_radius if len(self.data) > frame_radius + index_of_failure else len(
                self.data) - 1
        except Exception:
            successful = True
            start = 0
            end = len(self.data) - 1

        # builds the result for convenient access
        trial_frames = list(range(start, end + 1))
        sample_frames = [self.data[i]["frame_number"] for i in trial_frames]
        result_dict = self.visualize(trial_frames, sample_frames)
        zip_path = os.path.join(self.result_dir, 'result.zip')

        # writes raw result data as json, for future usage in the frontend
        json_path = os.path.join(self.result_dir, 'trial.json')
        with open(json_path, 'w') as f:
            json.dump(self.data, f)

        # writes short summary of the result for easy processing in the frontend
        result = {
            'success': successful,
            'fail_frame': index_of_failure
        }
        json_result_path = os.path.join(self.result_dir, 'result.json')
        with open(json_result_path, 'w') as f:
            json.dump(result, f)

        # zipping response files, for sending results as one file back to frontend
        with zipfile.ZipFile(zip_path, 'w') as myzip:
            myzip.write(result_dict['sample_path'])
            myzip.write(result_dict['trial_path'])
            myzip.write(json_path)
            myzip.write(json_result_path)
            myzip.close()

        return zip_path

    # builds 2 short clips out of the given trial and sample frames for visualisation of the detected error
    def visualize(self, trial_frames, sample_frames):
        """
        :param trial_frames: list of names of the trial_frames, that should be used for response Video
        :param sample_frames: list of names of the sample_frames, that should be used for response Video
        :return: void
        """

        #  builds variables for easier access later on
        sample_dir = os.path.join("./media", self.sample_id, 'skeletons')
        trial_dir = os.path.join('./media', 'temp_vid', 'skeletons')
        sample_frames = [os.path.join(sample_dir, str(x) + '.jpg') for x in sample_frames]
        trial_frames = [os.path.join(trial_dir, str(x) + '.jpg') for x in trial_frames]

        # reading images in respective arrays, for building the Video
        array_trial = []
        array_sample = []
        for frame_trial, frame_sample in zip(trial_frames, sample_frames):
            img_trial = cv2.imread(frame_trial)
            array_trial.append(img_trial)
            img_sample = cv2.imread(frame_sample)
            array_sample.append(img_sample)

        shape = array_trial[0].shape[1::-1]

        # building the trial Video snipped, for sending back to frontend
        trial_path = os.path.join(self.result_dir, 'trial.mp4')
        out_trail = cv2.VideoWriter(trial_path,
                                    cv2.VideoWriter_fourcc(*'mp4v'), 30, shape)
        for img in array_trial:
            out_trail.write(img)
        out_trail.release()

        # building the sample Video snipped, for sending back to frontend
        sample_shape = array_sample[0].shape[1::-1]
        sample_path = os.path.join(self.result_dir, 'sample.mp4')
        out_sample = cv2.VideoWriter(sample_path,
                                     cv2.VideoWriter_fourcc(*'mp4v'),
                                     30, sample_shape)
        for img in array_sample:
            out_sample.write(img)
        out_sample.release()

        # returning the paths for coping in response zip folder
        return {
            'sample_path': sample_path,
            'trial_path': trial_path
        }
