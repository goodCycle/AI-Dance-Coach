import os
import json
import codecs
import numpy as np


# TODO do the transformation the other way around?
class DifferenceCalculator:

    def __init__(self, sample_keypoint_path="media/video1/bodies"):
        self.sample_keypoint_path = sample_keypoint_path

        self.sample_keypoints = [json.load(codecs.open(filename, 'w', encoding='utf-8'), separators=(',', ':'))
                                 for filename in os.listdir(sample_keypoint_path)
                                 if filename.endswith(".json")]

    def __call__(self, *args, **kwargs):
        return self.list_difference(*args, **kwargs)

    def list_difference(self, keypoint_list):
        """
        :param keypoint_list: list of tuples (keypoints, corresponding_sample_frame) to compare to the sample
        :return: list of tuples (pose difference score dicts , corresponding_sample_frame)
        """
        bodypart_indicies = [
            {
                "name": "face",
                "indicies": [0, 15, 16, 17, 18],
                "weight": 1.0
            },
            {
                "name": "torso",
                "indicies": [1, 2, 3, 4, 5, 6, 7],
                "weight": 1.0
            },
            {
                "name": "legs",
                "indicies": [8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24],
                "weight": 1.0
            },
        ]

        return [(self.bin_difference(bodypart_indicies, keypoints, self.sample_keypoints[i]), i)
                for (keypoints, i) in keypoint_list]

    @staticmethod
    def bin_difference(bodypart_indicies,
                       keypoints_a,
                       keypoints_b):
        """

        :param bodypart_indicies: a mapping of bodyparts to keypoints (see the ?.json for more details)
        :param keypoints_a: pose in keypoint format
        :param keypoints_b: pose in keypoint format
        :return: the pose difference between the two poses for each bodypart as a dictionary (name: (score, weight))
        """

        def remove_confidence(x): return [[a, b] for [a, b, _] in x]

        def convert_to_2d_array(x): return np.array([np.array(xi) for xi in x])

        sample_features = convert_to_2d_array(remove_confidence(keypoints_a))
        input_features = convert_to_2d_array(remove_confidence(keypoints_b))

        score_dict = dict()

        for bodypart in bodypart_indicies:
            sample = sample_features[np.array(bodypart["indicies"])]
            input_ = input_features[np.array(bodypart["indicies"])]

            matrix = DifferenceCalculator.find_affine_matrix(input_, sample)
            transformed_input = DifferenceCalculator.affine_transform(matrix, input_)

            print("Input:")
            print(input_)
            print("A:")
            print(matrix)
            print("Result:")
            print(transformed_input)

            # normalizing the inputs for scoring
            sample = sample / np.linalg.norm(sample)
            transformed_input = transformed_input / np.linalg.norm(transformed_input)

            dist = np.linalg.norm(sample - transformed_input)
            # TODO get rotation between sample and transformed input
            score = dist

            score_dict[bodypart["name"]] = (score, bodypart["weight"])

        return score_dict

    @staticmethod
    def find_affine_matrix(input_features, sample_features):

        matrix, _, _, _ = np.linalg.lstsq(DifferenceCalculator.pad(input_features),
                                          DifferenceCalculator.pad(sample_features))
        matrix[np.abs(matrix) < 1e-11] = 0
        return matrix

    @staticmethod
    def affine_transform(matrix, input_vector):
        return np.dot(DifferenceCalculator.pad(input_vector), matrix)[:, :-1]

    @staticmethod
    def pad(x):
        return np.hstack([x, np.ones((x.shape[0], 1))])