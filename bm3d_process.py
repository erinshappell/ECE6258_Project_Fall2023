#################################################################################
### Denoising of challenging image datasets using BM3D
### Code written by Erin Shappell, for ECE 6258 Final Project
### Project Partner: Robert Pritchard
### The purpose of this script is to process a single dataset using BM3D, and
### record various IQA objective analyses of the results in a csv file.
#################################################################################

### Import libraries
import dippykit as dip
import numpy as np
import pandas as pd
import bm3d
import math
import glob
import os
import datetime

gt_subfolder_list  = [
                        '/0001_GT_SRGB/resized_gt/',
                        '/0002_GT_SRGB/resized_gt/',
                        '/0003_GT_SRGB/resized_gt/',
                        '/0051_GT_SRGB/resized_gt/',
                        '/0060_GT_SRGB/resized_gt/',
                        '/0080_GT_SRGB/resized_gt/',
                        '/0081_GT_SRGB/resized_gt/',
                        '/0101_GT_SRGB/resized_gt/',
                        '/0125_GT_SRGB/resized_gt/',
                        '/0150_GT_SRGB/resized_gt/',
                        '/0175_GT_SRGB/resized_gt/'
                     ]

subfolder_list      = [
                        '/0001_NOISY_SRGB/resized/',
                        '/0002_NOISY_SRGB/resized/',
                        '/0003_NOISY_SRGB/resized/',
                        '/0051_NOISY_SRGB/resized/',
                        '/0060_NOISY_SRGB/resized/',
                        '/0080_NOISY_SRGB/resized/',
                        '/0081_NOISY_SRGB/resized/',
                        '/0101_NOISY_SRGB/resized/',
                        '/0125_NOISY_SRGB/resized/',
                        '/0150_NOISY_SRGB/resized/',
                        '/0175_NOISY_SRGB/resized/'
                      ]

for ii in range(len(subfolder_list)):

    ### Print program start time
    now = datetime.datetime.now()
    print('------')
    print('| Program start time: ')
    print('| ' + now.strftime("%Y-%m-%d %H:%M:%S"))

    ### Load dataset
    ### This code was written to only load one folder of images at a time, as each of the datasets are very large
    ### home_path = base path to get to folder containing all datasets
    ### dataset   = name of dataset to analyze
    ### subfolder = name of the subfolder within the dataset to analyze (not analyzing the full set all at once)
    home_path      = '/Users/erinshappell/Dropbox (GaTech)/Coursework/Fall 2023/'
    dataset        = 'SIDD' # CURE-OR, CURE-TSR, CURE-TSD, SIDD, or Set12
    gt_subfolder   = gt_subfolder_list[ii]
    data_subfolder = subfolder_list[ii]
    gt_path        = home_path + dataset + gt_subfolder
    data_path      = home_path + dataset + data_subfolder

    ### Create directory for processed images
    proc_path = data_path + 'processed/'
    if not os.path.exists(proc_path): os.makedirs(proc_path)

    print('| Ground truth path: ' + gt_path)
    print('| Dataset path: ' + data_path)

    ### Get the names of all the images in the folder
    gt_img_names   = sorted(glob.glob(gt_path + '*.PNG'))
    data_img_names = sorted(glob.glob(data_path + '*.PNG'))
    num_imgs       = len(data_img_names)
    print('| Found %d images' % num_imgs)

    # Place a limit on how many images are analyzed at once
    limit = 1000
    if num_imgs > limit:
        num_imgs = limit
        gt_img_names   = gt_img_names[:limit]
        data_img_names = data_img_names[:limit]
        print('| Number of images exceeds limit of %d, program will stop once limit is reached' %limit)

    ### Initialize arrays for basic IQA metrics
    psnr = np.zeros(num_imgs)
    ssim = np.zeros(num_imgs)

    ### Process images using BM3D
    img_ct = 0   # counter to keep track of program progress

    # Main loop
    for ii in range(num_imgs):
        ### Load the ground truth image
        gt = dip.imread(gt_img_names[ii])

        ### Load the noisy image
        img = dip.imread(data_img_names[ii])

        ### Convert to grayscale (if necessary)
        if dataset != 'CURE-OR' and dataset != 'Set12':
            gt  = dip.rgb2gray(gt)
            img = dip.rgb2gray(img)

        img = dip.im_to_float(img)

        ### For the first image ONLY, estimate the noise PSD
        # Code snippet credit: https://stackoverflow.com/questions/2440504/noise-estimation-noise-measurement-in-image
        if img_ct == 0:
            filter = np.array([[1, -2, 1],
                                [-2, 4, -2],
                                [1, -2, 1]])
            sigma = np.sum(np.sum(np.absolute(dip.convolve2d(img, filter))))
            sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (img.shape[0] - 2) * (img.shape[1] - 2))
            if sigma == 0:
                print('| Sigma estimated to be 0 (likely in error). Will use 0.2 by default.')
                sigma = 0.2
            print('| Starting BM3D analysis with sigma = %.4f' % sigma)

        ### Process the image
        img_p = bm3d.bm3d(img,sigma)

        ### Calculate objective metrics
        ### PSNR
        img_p = dip.float_to_im(img_p)
        gt    = dip.float_to_im(gt)
        psnr[img_ct]   = dip.PSNR(img_p,gt)

        ### SSIM
        ssim[img_ct],_ = dip.SSIM(img_p,gt)

        # Save the image to get remaining metrics in MATLAB with provided code
        just_name = os.path.split(data_img_names[ii])[-1]
        dip.im_write(img_p, data_path + 'processed/' + os.path.splitext(just_name)[0] + '_proc.jpg')

        print('| Finished image %d' % img_ct)

        img_ct += 1 # update img counter

    ### Save calculated metrics to csv
    psnr = np.round(psnr, 4) # truncate to 4 decimal places
    ssim = np.round(ssim, 4) # truncate to 4 decimal places
    stacked = np.vstack((psnr,ssim)).T
    metrics = pd.DataFrame(stacked, columns=['psnr','ssim'])
    metrics.insert(0, 'filename', data_img_names)
    metrics.to_csv(data_path + 'processed/' + dataset + '_metrics.csv')

    ### Print program end time
    now = datetime.datetime.now()
    print('| Program end time: ')
    print('| ' + now.strftime("%Y-%m-%d %H:%M:%S"))
    print('------')

    gt_path        =  home_path + dataset + gt_subfolder
    data_path      =  home_path + dataset + data_subfolder

    ### Create directory for processed images
    proc_path = data_path + 'processed/'
    if not os.path.exists(proc_path): os.makedirs(proc_path)

    print('| Ground truth path: ' + gt_path)
    print('| Dataset path: ' + data_path)

    ### Get the names of all the images in the folder
    gt_img_names   = sorted(glob.glob(gt_path + '*.jpg'))
    data_img_names = sorted(glob.glob(data_path + '*.jpg'))
    num_imgs       = len(data_img_names)
    print('| Found %d images' % num_imgs)

    # Place a limit on how many images are analyzed at once
    limit = 1000
    if num_imgs > limit:
        num_imgs = limit
        gt_img_names   = gt_img_names[:limit]
        data_img_names = data_img_names[:limit]
        print('| Number of images exceeds limit of %d, program will stop once limit is reached' %limit)

    ### Initialize arrays for basic IQA metrics
    psnr = np.zeros(num_imgs)
    ssim = np.zeros(num_imgs)

    ### Process images using BM3D
    img_ct = 0   # counter to keep track of program progress

    # Main loop
    for ii in range(num_imgs):
        ### Load the ground truth image
        gt = dip.imread(gt_img_names[ii])

        ### Load the noisy image
        img = dip.imread(data_img_names[ii])

        ### Convert to grayscale (if necessary)
        if dataset != 'CURE-OR':
            gt  = dip.rgb2gray(gt)
            img = dip.rgb2gray(img)

        img = dip.im_to_float(img)

        ### For the first image ONLY, estimate the noise PSD
        # Code snippet credit: https://stackoverflow.com/questions/2440504/noise-estimation-noise-measurement-in-image
        if img_ct == 0:
            filter = np.array([[1, -2, 1],
                                [-2, 4, -2],
                                [1, -2, 1]])
            sigma = np.sum(np.sum(np.absolute(dip.convolve2d(img, filter))))
            sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (img.shape[0] - 2) * (img.shape[1] - 2))
            if sigma == 0:
                print('| Sigma estimated to be 0 (likely in error). Will use 0.2 by default.')
                sigma = 0.2
            print('| Starting BM3D analysis with sigma = %.4f' % sigma)

        ### Process the image
        img_p = bm3d.bm3d(img,sigma)

        ### Calculate objective metrics
        ### PSNR
        img_p = dip.float_to_im(img_p)
        gt    = dip.float_to_im(gt)
        psnr[img_ct]   = dip.PSNR(img_p,gt)

        ### SSIM
        ssim[img_ct],_ = dip.SSIM(img_p,gt)

        # Save the image to get remaining metrics in MATLAB with provided code
        just_name = os.path.split(data_img_names[ii])[-1]
        dip.im_write(img_p, data_path + 'processed/' + os.path.splitext(just_name)[0] + '_proc.jpg')

        print('| Finished image %d' % img_ct)

        img_ct += 1 # update img counter

    ### Save calculated metrics to csv
    psnr = np.round(psnr, 4) # truncate to 4 decimal places
    ssim = np.round(ssim, 4) # truncate to 4 decimal places
    stacked = np.vstack((psnr,ssim)).T
    metrics = pd.DataFrame(stacked, columns=['psnr','ssim'])
    metrics.insert(0, 'filename', data_img_names)
    metrics.to_csv(data_path + 'processed/' + dataset + '_metrics.csv')

    ### Print program end time
    now = datetime.datetime.now()
    print('| Program end time: ')
    print('| ' + now.strftime("%Y-%m-%d %H:%M:%S"))
    print('------')
