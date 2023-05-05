import numpy as np

import cv2
import sys

def ComputeWindowVarianceAndMean(image, window_size = 25):
	window_matrix = [];
	half_window = int(window_size/2);
	image_pad = np.pad(image, half_window, 'edge');
	
	for i in range(len(image_pad) - 2 * half_window):
		window_matrix_i = [];		
		for j in range(len(image_pad[i]) - 2 * half_window):
			window_matrix_i.append(image_pad[i:i+window_size, j:j+window_size].flatten());
		window_matrix.append(window_matrix_i);
	
	return np.array(window_matrix), np.mean(window_matrix, axis=-1), np.var(window_matrix, axis=-1), np.max(window_matrix, axis=-1), np.min(window_matrix, axis=-1);

def LCE(l_channel, window_size = 25, beta = 2):
	"""
	local color enhancement of L channel
	return the enhanced L channel
	"""
	
	var_g = np.var(l_channel);	
	L_w, u_b, var_b, L_max, L_min = ComputeWindowVarianceAndMean(l_channel, window_size);
	
	ratio = (np.ones(np.shape(var_b)) * var_g) / var_b;
	ratio[ratio > beta] = beta;
	
	L_EB = u_b + ratio * (l_channel.astype('float') - u_b);
	Lnorm_EB = (L_EB - L_min) / (L_max - L_min);
	
	L_EB_w, L_EB_u_b, _, _, _ = ComputeWindowVarianceAndMean(Lnorm_EB, window_size);
	Lnorm_w, Lnorm_u_b, Lnorm_var_b, _, _ = ComputeWindowVarianceAndMean(Lnorm_EB, window_size);
	
	k = np.mean((Lnorm_w * L_EB_w) - np.expand_dims(Lnorm_u_b * L_EB_u_b, axis=-1), axis=-1) / Lnorm_var_b;
	v = L_EB_u_b - k * Lnorm_u_b;
	
	Lgf_EB = k * L_EB + v;
	Lgf_EB[Lgf_EB < 0] = 0;
	Lgf_EB[Lgf_EB > 255] = 255;
	
	return Lgf_EB;

def CB(a_channel, b_channel, window_size = 25):
	"""
	color balance of a, b channel
	return the enhanced a, b channel
	like: return a_enhance, b_enhance
	"""
	
	means = [np.mean(a_channel), np.mean(b_channel)];
	ratio_a = (means[1] - means[0]) / (means[0] + means[1]);
	ratio_b = -ratio_a;
	
	if ratio_a > 0:
		a_channel = (1 + ratio_a) * a_channel;
	elif ratio_b > 0:
		b_channel = (1 + ratio_b) * b_channel;
	
	return a_channel, b_channel;


if __name__ == "__main__":
	import cv2
	sample = cv2.imread('images6.jpg')
	img_lab = cv2.cvtColor(sample, cv2.COLOR_BGR2LAB)

	a_enhance, b_enhance = CB(img_lab[:,:,1], img_lab[:,:,2], window_size = 25)
	img_lab[:,:,0] = LCE(img_lab[:,:,0], window_size = 25, beta = 2);
	img_lab[:,:,1] = a_enhance;
	img_lab[:,:,2] = b_enhance;

	result = cv2.cvtColor(img_lab, cv2.COLOR_LAB2BGR)

	cv2.imshow("result", result)
	if(cv2.waitKey(0)==27):
		cv2.destroyAllWindows()