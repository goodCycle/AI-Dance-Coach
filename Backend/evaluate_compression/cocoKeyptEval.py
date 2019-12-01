# Reference:
# https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoEvalDemo.ipynb

# import matplotlib.pyplot as plt
import sys
sys.path.append('/home/pose/cocoapi/PythonAPI')
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import numpy as np
# import skimage.io as io
from matplotlib import pylab
import pylab

class KeypointEval:
    def __init__(self, gt, detect):
        pylab.rcParams['figure.figsize'] = (10.0, 8.0)

        print('Running demo for keypoints results.')

        # initialize COCO ground truth api
        cocoGt=COCO(gt)

        # initialize COCO detections api
        cocoDt=cocoGt.loadRes(detect)

        imgIds=sorted(cocoGt.getImgIds())
        imgIds=imgIds[0:100]
#        imgId = imgIds[np.random.randint(100)]


        # run and prints evaluation results
        cocoEval = COCOeval(cocoGt,cocoDt,'bbox')
        cocoEval.params.imgIds  = imgIds
        cocoEval.evaluate()
        cocoEval.accumulate()
        cocoEval.summarize()
