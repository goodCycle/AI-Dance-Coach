import os
import json
import numpy as np


# TODO do the transformation the other way around?
class DifferenceCalculator:

    def __init__(self, sample_keypoint_path="./media/video1/bodies_keypoints"):
        self.sample_keypoint_path = sample_keypoint_path

        self.debug_frame= 0

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

        return [(self.bin_difference(bodypart_indicies, keypoints[0], self.sample_keypoints[i][0]), i)
                for (keypoints, i) in keypoint_list]

    #@staticmethod
    def bin_difference(self, bodypart_indicies,
                       keypoints_a,
                       keypoints_b):
        """

        :param bodypart_indicies: a mapping of bodyparts to keypoints (see the ?.json for more details)
        :param keypoints_a: pose in keypoint format
        :param keypoints_b: pose in keypoint format
        :return: the pose difference between the two poses for each bodypart as a dictionary (name: (score, weight))
        """

        def remove_confidence(x): return [[a[0], a[1]] for a in x]

        def convert_to_2d_array(x): return np.array([np.array(xi) for xi in x])

        removed_confidence_a = remove_confidence(keypoints_a)
        removed_confidence_b = remove_confidence(keypoints_b)

        sample_features = convert_to_2d_array(removed_confidence_a)
        input_features = convert_to_2d_array(removed_confidence_b)

        score_dict = dict()

        print(self.debug_frame)
        self.debug_frame += 1
        print("")

        for bodypart in bodypart_indicies:
            sample = sample_features[np.array(bodypart["indicies"])]
            input_ = input_features[np.array(bodypart["indicies"])]

            sample_clean = list()
            input_clean = list()

            for i, point in enumerate(sample):
                if np.linalg.norm(point) != 0 and np.linalg.norm(input_[i]) != 0:
                    sample_clean.append(point)
                    input_clean.append(input_[i])

            sample = np.array(sample_clean)
            input_ = np.array(input_clean)

            sample = sample / np.linalg.norm(sample)
            input_ = input_ / np.linalg.norm(input_)

            matrix = DifferenceCalculator.find_affine_matrix(input_, sample)
            transformed_input = DifferenceCalculator.affine_transform(matrix, input_)

            # print("Input:")
            # print(input_)
            # print("A:")
            # print(matrix)
            # print("Result:")
            # print(transformed_input)

            # normalizing the inputs for scoring
            #sample = sample / np.linalg.norm(sample)
            #transformed_input = transformed_input / np.linalg.norm(transformed_input)

            # determining rotation still buggy
            rot = np.degrees(
                -1 * np.arctan2(matrix[0][1] / np.linalg.norm(matrix[0]), matrix[0][0] / np.linalg.norm(matrix[0])))
            print(bodypart["name"] + " " + str(rot))

            # use max values instead of average?
            # dist = np.linalg.norm(sample - transformed_input)
            print("avg: "+str(np.linalg.norm(sample - transformed_input)))

            dist = 0
            distance_sum = 0
            counted_keypoints = 0

            for i, point in enumerate(sample):
                temp = np.linalg.norm(point - transformed_input[i])
                #print(point)
                #print(transformed_input)
                if np.linalg.norm(point) != 0 and np.linalg.norm(transformed_input[i]) != 0:
                    distance_sum += temp
                    counted_keypoints += 1
                    if temp > dist:
                        dist = temp
                else:
                    print("zero keypoints")

            if counted_keypoints == 0:
                counted_keypoints = 1
            score = dist #+ (distance_sum/counted_keypoints)
            if rot > 90 and rot < 150:
                score *= 0.25
            print("max+avg: " + str(score))

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
