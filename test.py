import cv2 
import matlab.engine
from MLLE import *
from evaluation.uiqm_utils import *


def PCQI(img, img_result):
  global eng
  img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img_result_g = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
  return eng.PCQI(img_g, img_result_g)

def CCF(img_result):
  global eng
  img_rgb = cv2.cvtColor(img_result,cv2.COLOR_BGR2RGB)
  return eng.CCF(img_rgb)

def AG(img_result):
  global eng
  img_result_g = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
  return eng.AG(img_result_g)

def EI(img_result):
  global eng
  img_result_g = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
  return eng.EI(img_result_g)

eng = matlab.engine.start_matlab()
eng.addpath('evaluation/')
eng.addpath('evaluation/PCQI/')
eng.addpath('evaluation/CCF-master/')
img, filename = getimg()

img_result = MLLE(img, filename)
print(getUIQM(img_result))
print(PCQI(img, img_result))
print(CCF(img_result))
print(AG(img_result))
print(EI(img_result))
