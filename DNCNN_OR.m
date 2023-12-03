%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Code for processing large images with DnCNN and upsamples if needed. Code
% iterates through all folders within dataset_folder and saves the result
% to folders of the same name in save_path
%
% Author: Robert Pritchard
% Project Partner: Erin Shappell
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc;
clear;
addpath('Code');
dataset_folder = 'D:\ECE6258_Project\CURE-TSD_last/01_04_01_08_01/';

image_path = dataset_folder;

save_path = 'Results/CURE-TSD_last/01_04_01_08_01/';


file_list = dir(dataset_folder);
file_list = file_list(3:end);
mkdir(save_path(1:end-1))
net = denoisingNetwork("dncnn");
for i = 1:length(file_list)
    

    nI = im2gray(imread([image_path,file_list(i).name]));
    sz = size(nI);
    if min(sz)<256
        ratio = ceil(256/max(sz));
        nI = imresize(nI,ratio,'bilinear');
    end
    
    d_im = denoiseImage(nI,net);
    disp(i)
    if min(sz)<256
        d_im = imresize(d_im,1/ratio,"nearest");
    end
    imwrite( d_im,[save_path,file_list(i).name] );
end

