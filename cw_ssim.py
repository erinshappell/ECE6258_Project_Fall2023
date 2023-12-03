#################################################################################
### Calculation of CW-SSIM of images processed with BM3D
### Code written by Erin Shappell, for ECE 6258 Final Project
### Project Partner: Robert Pritchard
### The purpose of this script is to calculate CW-SSIM for a folder of images
### already denoised using the script bm3d_process.py
#################################################################################

### Import libraries
import numpy as np
import pandas as pd
import glob
import os
import datetime
from ssim import SSIM
from PIL import Image # this implementation of cw-ssim requires Pillow for image I/O

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
dataset        = 'CURE-OR'
gt_subfolder   = '/10_grayscale_no_challenge/3d1/HTC/'
proc_subfolder = '/18_grayscale_saltpepper/Level_1/3d1/HTC/processed/'
gt_path        =  home_path + dataset + gt_subfolder
proc_path      =  home_path + dataset + proc_subfolder

### Get the names of all the images in the folder
gt_img_names = glob.glob(gt_path + '*.jpg')
proc_img_names = glob.glob(proc_path + '*.jpg')
num_imgs = len(proc_img_names)
print('| Found %d images' % num_imgs)

### Calculate CW-SSIM
cw_ssim = np.zeros(num_imgs)
img_ct  = 0   # counter to keep track of program progress
print('| Starting CW-SSIM calculations')

for ii in range(num_imgs):
    ### Load the ground truth image
    gt = Image.open(gt_img_names[ii])
    gt = gt.convert('L') # convert to grayscale

    ### Load the processed image
    img_p = Image.open(proc_img_names[ii])

    ### Calculate CW-SSIM
    cw_ssim[img_ct] = SSIM(gt).cw_ssim_value(img_p)

    print('| Finished image %d' % img_ct)

    img_ct += 1 # update img counter

### Append to main csv containing results from all IQA metrics
metrics = pd.read_csv(proc_path + dataset + '_metrics.csv')
metrics['cw-ssim'] = cw_ssim
metrics.to_csv(proc_path + dataset + '_metrics.csv')

### Print program end time
now = datetime.datetime.now()
print('| Program end time: ')
print('| ' + now.strftime("%Y-%m-%d %H:%M:%S"))
print('------')
