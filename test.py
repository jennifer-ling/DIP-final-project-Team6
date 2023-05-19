import cv2 
from MLLE import *
from evaluation.uiqm_utils import *


img, filename = getimg()
img_result = MLLE(img, filename, True)
print(getUIQM(img_result))