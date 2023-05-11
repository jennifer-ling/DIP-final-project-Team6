import numpy as np
import cv2

def MCLP(img):
  """
  input: original image
  output: color transfer image
  """
  # Convert image to float for calculations
    img = img.astype(np.float32)
  # Split image into color channels
    B, G, R = cv2.split(img)
    mean_B, mean_G, mean_R = np.mean(B), np.mean(G), np.mean(R)
    
    # Define the color channels of the largest mean value, medium mean value, and smallest mean value
    color_means = {"B": mean_B, "G": mean_G, "R": mean_R}
    sorted_colors = sorted(color_means.items(), key=lambda x: x[1])
    I_s, I_m, I_l = sorted_colors[0][0], sorted_colors[1][0], sorted_colors[2][0]    
  
    # Apply the color correction
    I_l_cr = 255 * (I_l - np.min(I_l, axis=(0, 1))) / (np.max(I_l, axis=(0, 1)) - np.min(I_l, axis=(0, 1)))


    while True:
        I_m_cr = I_m + (np.mean(I_l) - np.mean(I_m)) * I_l
        I_s_cr = I_s + (np.mean(I_l) - np.mean(I_s)) * I_l
        
        # Check for convergence
        loss = abs(np.mean(I_l) - np.mean(I_m)) + abs(np.mean(I_l) - np.mean(I_s))
        if loss < 1e-2:
            break

        I_m, I_s = I_m_cr, I_s_cr

    # Merge the color corrected channels
    img_ct = cv2.merge([I_s_cr, I_m_cr, I_l_cr]).astype(np.uint8)
    
    return img_ct

def MAMGF(img_origin, img_ct):
  """
  input: original image and color transfer image
  output: color corrected image
  """
  # Convert image to float for calculations
    img_origin = img_origin.astype(np.float32)
    img_ct = img_ct.astype(np.float32)
    
    # Apply the max attenuation map
    gamma = 1.2
    A_max_M = np.max([1 - img_origin[..., i] ** gamma for i in range(3)], axis=0)
    
    # Apply the color correction
    D = img_origin - cv2.GaussianBlur(img_origin, (3, 3), 0)
    I_cc = D + A_max_M[..., None] * img_ct + (1 - A_max_M[..., None]) * img_origin
    
    return I_cc.astype(np.uint8)  
