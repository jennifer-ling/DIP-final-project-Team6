import numpy as np
import time
import cv2
import sys

def ComputeWindowVarianceAndMean(image, window_size = 25, flags = [True, True, True]):
	L_w = np.zeros((np.shape(image)[0], np.shape(image)[1], window_size**2), dtype = 'float32');	
	half_window = int(window_size/2);
	image_pad = np.pad(image, half_window, 'edge');
	
	for i in range(len(image_pad) - 2 * half_window):
		for j in range(len(image_pad[i]) - 2 * half_window):
			L_w[i, j] = image_pad[i:i+window_size, j:j+window_size].flatten();
	
	'''
	weight = 1 / (window_size**2);
	summed_area_table = np.pad(image_pad.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), 'constant', constant_values=0);
	for row_index in range(np.shape(u_b)[0]):
		for col_index in range(np.shape(u_b)[1]):
			u_b[row_index, col_index] = weight * (summed_area_table[row_index, col_index] + summed_area_table[row_index+window_size, col_index+window_size] - summed_area_table[row_index, col_index+window_size] - summed_area_table[row_index+window_size, col_index]);
	'''
	u_b = np.mean(L_w, axis=-1);
	var_b = np.var(L_w, axis=-1) if flags[0] else None;
	L_max = np.max(L_w, axis=-1) if flags[1] else None;
	L_min = np.min(L_w, axis=-1) if flags[2] else None;
	
	return L_w, u_b, var_b, L_max, L_min;
	

def LCE(l_channel, window_size = 25, beta = 2):
	"""
	local color enhancement of L channel
	return the enhanced L channel
	"""
	eps = np.finfo('float').eps;
	var_g = np.var(l_channel);	
	L_w, u_b, var_b, L_max, L_min = ComputeWindowVarianceAndMean(l_channel, window_size, [True, True, True]);
	
	ratio = (np.ones(np.shape(var_b)) * var_g) / (var_b + eps);
	ratio[ratio > beta] = beta;
	
	L_EB = u_b + ratio * (l_channel.astype('float') - u_b);
	Lnorm_EB = (L_EB - L_min) / (L_max - L_min + eps);
	
	L_EB_w, L_EB_u_b, _, _, _ = ComputeWindowVarianceAndMean(Lnorm_EB, window_size, [False, False, False]);
	Lnorm_w, Lnorm_u_b, Lnorm_var_b, _, _ = ComputeWindowVarianceAndMean(Lnorm_EB, window_size, [True, False, False]);
	
	k = np.mean((Lnorm_w * L_EB_w) - np.expand_dims(Lnorm_u_b * L_EB_u_b, axis=-1), axis=-1) / (Lnorm_var_b + eps);
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
	eps = np.finfo('float').eps;
	means = [np.mean(a_channel), np.mean(b_channel)];
	ratio_a = (means[1] - means[0]) / (means[0] + means[1] + eps);
	ratio_b = -ratio_a;
	
	if ratio_a > 0:
		a_channel = (1 + ratio_a) * a_channel;
	elif ratio_b > 0:
		b_channel = (1 + ratio_b) * b_channel;
	
	return a_channel, b_channel;


if __name__ == "__main__":
	import cv2
	
	sample = cv2.imread('testcase/images6.jpg')
	
	img_lab = cv2.cvtColor(sample, cv2.COLOR_BGR2LAB)
	
	a_enhance, b_enhance = CB(img_lab[:,:,1], img_lab[:,:,2], window_size = 25)
	t = time.time()
	img_lab[:,:,0] = LCE(img_lab[:,:,0], window_size = 25, beta = 2);
	print(time.time()-t)
	img_lab[:,:,1] = a_enhance;
	img_lab[:,:,2] = b_enhance;

	result = cv2.cvtColor(img_lab, cv2.COLOR_LAB2BGR)
	
	cv2.imshow("result", result)
	cv2.imwrite("result.png", result)
	if(cv2.waitKey(0)==27):
		cv2.destroyAllWindows()