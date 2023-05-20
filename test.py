import cv2 
import matlab.engine
from MLLE import *
from evaluation.uiqm_utils import *


def PCQI(img, img_result):
  img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img_result_g = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
  eng = matlab.engine.start_matlab()
  eng.addpath('evaluation/PCQI/')
  return eng.PCQI(img_g, img_result_g)

def CCF(img_result):
  img_rgb = cv2.cvtColor(img_result,cv2.COLOR_BGR2RGB)
  eng = matlab.engine.start_matlab()
  eng.addpath('evaluation/CCF-master/')
  return eng.CCF(img_rgb)

img, filename = getimg()
img_result = MLLE(img, filename, True)
print(getUIQM(img_result))
print(PCQI(img, img_result))
# print(CCF(img_result))

