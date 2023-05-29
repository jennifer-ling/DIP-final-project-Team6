import cv2 
import matlab.engine
import numpy as np
import os
import sys
import argparse
from MLLE import *
from evaluation.uiqm_utils import *


def parse_arg():
  """
  read the file name, and sample size
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--filename", type=str, default="test")
  parser.add_argument("-s", "--size", type=int, default=15)
  parser.add_argument("-d", "--demo", action="store_true", default=False)
  args = parser.parse_args()
  return args.filename, args.size, args.demo

def UIQM(img_result, *_):
  img_rgb = cv2.cvtColor(img_result,cv2.COLOR_BGR2RGB)
  return getUIQM(img_rgb)

def PCQI(img_result,img):
  global eng
  img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img_result_g = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
  return eng.PCQI(img_g, img_result_g)

def CCF(img_result,*_):
  global eng
  img_rgb = cv2.cvtColor(img_result,cv2.COLOR_BGR2RGB)
  return eng.CCF(img_rgb)

def AG(img_result, *_):
  global eng
  img_result_g = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
  return eng.AG(img_result_g)

def EI(img_result, *_):
  global eng
  img_result_g = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
  return eng.EI(img_result_g)

def MLLE_paper(img):
  global eng
  img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  img_lacc = eng.LACC(img_rgb)
  img_result = eng.LACE(img_lacc)
  # print(np.array(img_result).shape)
  return cv2.cvtColor(np.array(img_result), cv2.COLOR_RGB2BGR)

def printEval(evaluations, path,size=1):
  print(f"==={path}===")
  for evaluation in evaluations:
    for k, v in evaluation.items():
      print(f"{k.__name__}: {round(v/size,3)}", end=" ")
      evaluation[k] = 0
    print()
  print()

# config of matlab engine
eng = matlab.engine.start_matlab()
eng.addpath('evaluation/')
eng.addpath('evaluation/PCQI/')
eng.addpath('evaluation/CCF-master/')
eng.addpath('MMLE_code-main/2022-MLLE/Method')

# config of datasets path
dataset = {
          "UIQS/": ('A/', 'B/', 'C/', 'D/', 'E/'), 
          "UCCS/":("blue/", "blue-green/", "green/"),
          "UIEB_raw": ("/"),
          }

# parse input
out_file, size, mode = parse_arg()
sys.stdout = open(f"{out_file}.txt", "w+")
sample_size = [size//5]*5 + [size//3]*3 + [size]

if mode:
  data_folder_path = ['testcase/demo/']
else: 
  data_folder_path = ['testcase/'+ i[0] + j  for i in dataset.items() for j in i[1]]

# set random seed
np.random.seed(0)

# traverse data datafolder
for i, path in enumerate(data_folder_path):
  if mode:
    images = os.listdir(path)
  else:
    images = np.random.choice(os.listdir(path), sample_size[i], replace=False)
  # evaluation = [[0]*5]*2
  # function list
  func = [AG, EI, PCQI, UIQM, CCF]
  evaluation = [dict.fromkeys(func, 0), dict.fromkeys(func, 0)]
  for image in images:
    img = cv2.imread(path+image)
    # apply MLLE
    img_result = [MLLE(img), MLLE_paper(img)]
    for ind in (0,1):
      for fn in func:
        evaluation[ind][fn] += fn(img_result[ind], img)
    if mode:
      printEval(evaluation, image)
  if not mode:
    printEval(evaluation, path, sample_size[i])
