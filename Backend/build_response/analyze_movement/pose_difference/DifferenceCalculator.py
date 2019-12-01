import os
import json
import numpy as np


class DifferenceCalculator:
    """
    Calculates the pose differences between two sequences of body pose keypoints,
    the sample being provided as a filepath to the corresponding numpy files for the keypoints,
    the user video frames being provided as a list (one item per frame) of keypoints
    """

    def __init__(self, sample_keypoint_path="./media/video1/bodies_keypoints"):
        self.sample_keypoint_path = sample_keypoint_path
        self.debug_frame = 0
        self.sample_keypoints = [np.load(self.sample_keypoint_path + "/" + filename)
                                 for filename in os.listdir(sample_keypoint_path)]

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
                "weight": 0.0
            },
            {
                "name": "body",
                "indicies": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24],
                "weight": 1.0
            },
            {
                "name": "legs",
                "indicies": [8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24],
                "weight": 0.0
            },
        ]

        # fix length mismatch between sample and input video
        if len(keypoint_list) > len(self.sample_keypoints):
            keypoint_list = keypoint_list[:(len(self.sample_keypoints)-1)]

        # apply the binary difference calculation to all frame pairs
        return [(self.bin_difference(bodypart_indicies, keypoints[0], self.sample_keypoints[i][0]), i)
                for (keypoints, i) in keypoint_list]

    def bin_difference(self, bodypart_indicies,
                       keypoints_a,
                       keypoints_b):
        """Calculate the pose difference between two sets of body keypoints

        :param bodypart_indicies: a mapping of bodyparts to keypoints (see the ?.json for more details)
        :param keypoints_a: pose in keypoint format
        :param keypoints_b: pose in keypoint format
        :return: the pose difference between the two poses for each bodypart as a dictionary (name: (score, weight))
        """

        def remove_confidence(x): return [[a[0], a[1]] for a in x]

        def convert_to_2d_array(x): return np.array([np.array(xi) for xi in x])

        # reshape the input and sample for the linear transformations
        removed_confidence_a = remove_confidence(keypoints_a)
        removed_confidence_b = remove_confidence(keypoints_b)
        sample_features = convert_to_2d_array(removed_confidence_a)
        input_features = convert_to_2d_array(removed_confidence_b)

        score_dict = dict()

        # Debug outputs for testing tresholds
        print("")
        print(self.debug_frame)
        self.debug_frame += 1
        print("")

        for bodypart in bodypart_indicies:

            # filter the relevant keypoint indicies for the body parts
            sample = sample_features[np.array(bodypart["indicies"])]
            input_ = input_features[np.array(bodypart["indicies"])]

            sample_clean = list()
            input_clean = list()

            # eliminate keypoints where OpenPose was unable to detect the point in one of the images
            for i, point in enumerate(sample):
                if np.linalg.norm(point) != 0 and np.linalg.norm(input_[i]) != 0:
                    sample_clean.append(point)
                    input_clean.append(input_[i])

            sample = np.array(sample_clean)
            input_ = np.array(input_clean)

            # normalize inputs for processing
            sample = sample / np.linalg.norm(sample)
            input_ = input_ / np.linalg.norm(input_)

            # find affine matrix and apply the transformation
            matrix = DifferenceCalculator.find_affine_matrix(input_, sample)
            transformed_input = DifferenceCalculator.affine_transform(matrix, input_)

            # determining rotation for debugging, will require future work
            rot = np.degrees(
                -1 * np.arctan2(matrix[0][1] / np.linalg.norm(matrix[0]), matrix[0][0] / np.linalg.norm(matrix[0])))
            print(bodypart["name"] + " " + str(rot))

            # find biggest difference between a pair of keypoints
            dist = 0
            for i, point in enumerate(sample):
                temp = np.linalg.norm(point - transformed_input[i])
                if np.linalg.norm(point) != 0 and np.linalg.norm(transformed_input[i]) != 0:
                    if temp > dist:
                        dist = temp
                else:
                    print("zero keypoints - filtering error")

            score = dist + np.linalg.norm(sample - transformed_input)

            if 150 > rot > 90:  # filter out anomalies caused by faulty keypoints
                score *= 0.25

            print("max+avg: " + str(score))
            score_dict[bodypart["name"]] = (score, bodypart["weight"])

        return score_dict

    @staticmethod
    def find_affine_matrix(input_features, sample_features):
        """Finds a transformation that results in the least squared error between
         the transformation of the input_features and the sample features

        :param input_features: pose keypoints to be transformed
        :param sample_features: target pose keypoints
        :return: The affine transformation matrix
        """
        matrix, _, _, _ = np.linalg.lstsq(DifferenceCalculator.pad(input_features),
                                          DifferenceCalculator.pad(sample_features))
        matrix[np.abs(matrix) < 1e-11] = 0
        return matrix

    @staticmethod
    def affine_transform(matrix, input_vector):
        """Apply the affine transformation matrix to the input vector"""
        return np.dot(DifferenceCalculator.pad(input_vector), matrix)[:, :-1]

    @staticmethod
    def pad(x):
        """reshaping of the input matrix x to make the calculation of the affine matrix possible"""
        return np.hstack([x, np.ones((x.shape[0], 1))])
