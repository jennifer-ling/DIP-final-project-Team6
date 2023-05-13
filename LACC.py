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
        # I_l = 255 * (I_l - np.min(I_l)) / (np.max(I_l) - np.min(I_l))
        I_m = I_m + (np.mean(I_l) - np.mean(I_m)) * I_l
        I_m = np.min(I_l)+(I_m-np.min(I_m))*(np.max(I_l)-np.min(I_l))/(np.max(I_m)-np.min(I_m))
        # I_m = cv2.normalize(I_m, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)


        I_s = I_s + (np.mean(I_l) - np.mean(I_s)) * I_l
        I_s = np.min(I_l)+(I_s-np.min(I_s))*(np.max(I_l)-np.min(I_l))/(np.max(I_s)-np.min(I_s))
        # I_s = cv2.normalize(I_s, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        loss = abs(np.mean(I_l) - np.mean(I_m)) + abs(np.mean(I_l) - np.mean(I_s))
        print("loss= ", loss)
        if loss < 1e-2:  # Check for convergence
            break
    # print("Im=",I_m)
    # print("Is=",I_s)


    I_l = cv2.normalize(I_l, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    I_m = cv2.normalize(I_m, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    I_s = cv2.normalize(I_s, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imwrite('I_l.jpg', I_l)
    cv2.imwrite('I_m.jpg', I_m)
    cv2.imwrite('I_s.jpg', I_s)


    # Merge the color corrected channels
    color_channels = {color_s: I_s, color_m: I_m, color_l: I_l}
    img_ct = cv2.merge([color_channels['B'], color_channels['G'], color_channels['R']]).astype(np.uint8)
    cv2.imwrite('img_ct.jpg', img_ct)
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
    gamma = 0.1
    A_max_M = np.max([1 - img_origin[..., i] ** gamma for i in range(3)], axis=0)

    # Apply the color correction
    cv2.imwrite('img_origin.jpg',img_origin)
    D = img_origin - cv2.GaussianBlur(img_origin, (111, 111), 0)
    # D_normalized = cv2.normalize(D, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    A_max_M_normalized = cv2.normalize(A_max_M, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # cv2.imwrite('D.jpg', D_normalized)
    # cv2.imwrite('A_max_M.jpg', A_max_M_normalized)
    I_cc = D + A_max_M[..., None] * img_ct + (1 - A_max_M[..., None]) * img_origin
    # I_cc = D_normalized + A_max_M_normalized[..., None] * img_ct + (1 - A_max_M_normalized[..., None]) * img_origin


    I_cc_normalized = cv2.normalize(I_cc, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imwrite('I_cc.jpg', I_cc_normalized)

    return I_cc.astype(np.uint8)
