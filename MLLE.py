import cv2
import numpy as np
import argparse
from LACC import *
from LACE import *


def getimg():
  """
  read the file name specified in the command line
  open the image file, and return it
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("inputimg")
  parser.add_argument("outputimg")
  inputname = "testcase/" + parser.parse_args().inputimg
  outputname = "result/" + parser.parse_args().outputimg
  return cv2.imread(inputname), outputname

def MLLE(img, filename="test", write_mode=False):
  img_ct = MCLP(img.copy())
  img_cr = MAMGF(img.copy(), img_ct.copy())
  l_channel, a_channel, b_channel = cv2.split(cv2.cvtColor(img_cr, cv2.COLOR_BGR2LAB))
  l_enhance = LCE(l_channel.copy())
  a_enhance, b_enhance = CB(a_channel.copy(), b_channel.copy())
  img_final = cv2.cvtColor(cv2.merge([l_enhance.astype(np.uint8), a_enhance.astype(np.uint8), b_enhance.astype(np.uint8)]), cv2.COLOR_LAB2BGR)
  if write_mode:
    cv2.imwrite(f"{filename}_ct.png", img_ct)
    cv2.imwrite(f"{filename}_cr.png", img_cr)
    cv2.imwrite(f"{filename}_final.png", img_final)
  return img_final


if __name__ == "__main__":
  img, filename = getimg()
  
  cv2.imwrite("test.png",MLLE(img, filename, write_mode=True))

