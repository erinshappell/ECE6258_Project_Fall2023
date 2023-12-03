%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Code for processing large images with DnCNN using block processing. Code
% iterates through all folders within dataset_folder and saves the result
% to folders of the same name in save_path
% Author: Robert Pritchard
% Project Partner: Erin Shappell
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc;
clear;
addpath('Code');
dataset_folder = 'D:\ECE6258_Project\CURE-TSD_last';
folders = dir(dataset_folder);
folders = folders(3:end);

for f = 1:length(folders)
    if ~isempty(strfind(folders(f).name, "GT"))
            continue
    end
    image_path = [dataset_folder,'/',folders(f).name,'/'];

        disp(image_path)
    save_path = ['Results/CURE-TSD_leftover/',folders(f).name,'/'];
    disp(save_path)
    profile  =   'normal';   
    v        =   15;
    
    file_list = dir([image_path,'*.jpg']);
    mkdir(save_path(1:end-1))
    mkdir([save_path,'Gray'])
    net = denoisingNetwork("dncnn");
    netfun = @(block_struct) denoiseImage(block_struct.data,net);
    for i = 1:length(file_list)
        nI = im2gray(imread([image_path,file_list(i).name]));
        sz = size(nI);
        if min(sz)<256
            ratio = ceil(256/max(sz));
            nI = imresize(nI,ratio,'bilinear');
        end
        imwrite(nI,[save_path,'Gray/',file_list(i).name,'_gray.tif'])
        disp('start')
        tic
        d_im = blockproc(string([save_path,'Gray/',file_list(i).name,'_gray.tif']),[1024,1024],netfun);
        toc
        disp('done')
        if min(sz)<256
            d_im = imresize(d_im,1/ratio,"nearest");
        end
        imwrite( d_im,[save_path,file_list(i).name] );
    end

end
