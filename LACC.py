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
    I_s, I_m, I_l = None, None, None
    color_s, color_m, color_l = None, None, None

    for idx, (color, mean) in enumerate(sorted_colors):
        if idx == 0:  # Smallest mean value
            if color == "B":
                I_s = B
                color_s = "B"

            elif color == "G":
                I_s = G
                color_s = "G"
            else:
                I_s = R
                color_s = "R"

        elif idx == 1:  # Medium mean value
            if color == "B":
                I_m = B
                color_m = "B"
            elif color == "G":
                I_m = G
                color_m = "G"
            else:
                I_m = R
                color_m = "R"
        else:  # Largest mean value
            if color == "B":
                I_l = B
                color_l = "B"
            elif color == "G":
                I_l = G
                color_l = "G"
            else:
                I_l = R
                color_l = "R"
    # Apply the color correction
    while True:

        # Apply the color correction
        I_m = I_m + (np.mean(I_l) - np.mean(I_m)) * I_l/255
        I_s = I_s + ((np.mean(I_l) - np.mean(I_s)) * I_l/255 + (np.mean(I_m) - np.mean(I_s)) * I_m/255)/2
        loss = abs(np.mean(I_l) - np.mean(I_m)) + abs(np.mean(I_l) - np.mean(I_s))
        if loss < 1e-2:  # Check for convergence
            break

    I_l = cv2.normalize(I_l, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    I_m = np.clip(I_m, 0, 255).astype(np.uint8)
    I_s = np.clip(I_s, 0, 255).astype(np.uint8)
    I_m = cv2.normalize(I_m, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    I_s = cv2.normalize(I_s, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Merge the color corrected channels
    color_channels = {color_s: I_s, color_m: I_m, color_l: I_l}
    img_ct = cv2.merge([color_channels['B'].astype(np.uint8), color_channels['G'].astype(np.uint8), color_channels['R'].astype(np.uint8)]).astype(np.uint8)
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
    gamma= 1.2
    A_max_M = np.max([1 - (img[..., i]/255) ** gamma for i in range(3)], axis=0)

    # Apply the color correction
    D = img_origin - cv2.GaussianBlur(img_origin, (21, 21), 1.5)
    I_cc = D + A_max_M[..., None] * img_ct + (1 - A_max_M[..., None]) * img_origin
    return I_cc.astype(np.uint8)
