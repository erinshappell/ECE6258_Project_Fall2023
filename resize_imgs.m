%% RESIZE
% Script written by Erin Shappell for ECE 6258
% Script will resize all images in a folder by a user-defined factor

%% Read in images
% gt_imgs: original images
% pr_imgs: processed images
home_path      = '/Users/erinshappell/Dropbox (GaTech)/Coursework/Fall 2023/';
dataset        = 'CURE-TSD';
%gt_subfolder   = '/GT/01_04_00_00_00/'
proc_subfolder = '/analyze/Scene4/01_04_01_09_01/';
%gt_path        = append(home_path,dataset,gt_subfolder);
data_path      = append(home_path,dataset,proc_subfolder);
proc_gt_path   = append(gt_path,'resized_gt/');
proc_path      = append(data_path,'resized/');
%gt_imgs        = dir(append(gt_path,'*jpg'));
data_imgs      = dir(append(data_path,'*jpg'));
num_imgs       = length(data_imgs);    % Number of images found
fprintf('| Found %d images\n', num_imgs);

%% Run resizing for all images in folder

mkdir(proc_gt_path)
mkdir(proc_path)
resize_factor = 1/2;
fprintf('| Starting resizing \n')
unique = zeros(num_imgs,1);
for ii = 1 : num_imgs
    % load images
    %gt_imgname   = gt_imgs(ii).name;
    data_imgname = data_imgs(ii).name;
    %gt_img       = imread(append(gt_path,gt_imgname));
    data_img     = imread(append(data_path,data_imgname));
    
    % resize
    %gt_img   = imresize(gt_img,resize_factor);
    data_img = imresize(data_img,resize_factor);
     
    % save resized images
    %imwrite(gt_img, append(proc_gt_path,'resized_',gt_imgname));
    imwrite(data_img, append(proc_path,'resized_',data_imgname));
    
    fprintf('| Finished image %d \n', ii);

end
