%%%%%%%%This is a demo for the usage of PCQI with default settings%%%%%%%%%%%%%%%%%%
clc;
clear;

im1=imread('ref.png');
im2=imread('contrast_changed.png');

im1=double(rgb2gray(im1));
im2=double(rgb2gray(im2));

[mpcqi,pcqi_map]=PCQI(im1,im2);

