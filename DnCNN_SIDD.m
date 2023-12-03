%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Code for processing large images with DnCNN and upsamples if needed. Code
% iterates through all folders within dataset_folder and saves the result
% to folders of the same name in save_path. This code is changed to iterate
% through SIDD file system 
%
% Author: Robert Pritchard
% Project Partner: Erin Shappell
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc;
clear;
addpath('Code');
dataset_folder = 'D:\ECE6258_Project\SIDD';
folders = dir(dataset_folder);
folders = folders(3:end);

for f = 1:length(folders)
    if ~isempty(strfind(folders(f).name, "GT"))
            continue
    end
    image_path = [dataset_folder,'/',folders(f).name,'/resized/'];

        disp(image_path)
    save_path = ['Results/SIDD_small/',folders(f).name,'/'];
    disp(save_path)
    mkdir(save_path)
    
    file_list = dir([image_path,'*.PNG']);
    net = denoisingNetwork("dncnn");
    for i = 1:length(file_list)
        nI = imread([image_path,file_list(i).name]);
        disp('start')
        tic
        d_im = denoiseImage(nI,net);
        toc
        disp('done')
        imwrite( d_im,[save_path,file_list(i).name] );

    end

end
