%% SUMMER
% Script written by Erin Shappell for ECE 6258
% Based on original script: SUMMER.m by Dogancan Temel
% Script will run SUMMER for all images within a folder and save
% the values to csv

%% Read in images
% gt_imgs: original images
% pr_imgs: processed images

home_path      = '/Users/erinshappell/Dropbox (GaTech)/Coursework/Fall 2023/';
dataset        = 'CURE-TSR';
gt_subfolder   = '/Real_Test/ChallengeFree/';
proc_subfolder = '/Real_Test/DirtyLens-1/processed/';
gt_path        = append(home_path,dataset,gt_subfolder);
proc_path      = append(home_path,dataset,proc_subfolder);
gt_imgs        = dir(append(gt_path,'*bmp'));
proc_imgs      = dir(append(proc_path,'*jpg'));
num_imgs       = length(proc_imgs);    % Number of images found
fprintf('| Found %d images\n', num_imgs);

%% Run SUMMER
% Call summer which returns the perceived quality. 

fprintf('| Starting SUMMER analysis\n')
summer_vals = zeros(num_imgs,1);
for ii = 1 : num_imgs
    % load images
    gt_imgname   = gt_imgs(ii).name;
    proc_imgname = proc_imgs(ii).name;
    gt_img       = imread(append(gt_path,gt_imgname));
    proc_img     = imread(append(proc_path,proc_imgname));
    
    % convert gt images to grayscale first if not already
    gt_img   = rgb2gray(gt_img);
    
    % convert grayscale images to rgb space
    map      = hsv(256);
    gt_img   = ind2rgb(gt_img,map);
    proc_img = ind2rgb(proc_img,map);   
  
    % run SUMMER
    summer_vals(ii) = SUMMER(gt_img,proc_img);
    fprintf('| Finished image %d \n', ii);
end

% Write SUMMER values to csv
writematrix(summer_vals,append(proc_path,'SUMMER.csv'));
