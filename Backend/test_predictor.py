# Run this from the root directory
import sys
import os

from posewrapper.PosePredictor import PosePredictor

print(PosePredictor(model="../../openpose/models/").predict_image("./images/10.jpg"))
