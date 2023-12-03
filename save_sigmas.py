#################################################################################
### Calculating noise PSD used in BM3D denoising
### Code written by Erin Shappell, for ECE 6258 Final Project
### Project Partner: Robert Pritchard
### The purpose of this script is to calculate and save the value of sigma used
### for each BM3D processing session
#################################################################################

### Import libraries
import dippykit as dip
import numpy as np
import pandas as pd
import math
import glob
import datetime

### List of all data subfolders
subfolder_list = [
                  'CURE-OR/12_grayscale_underexposure/Level_1/3d1/HTC/',
                  'CURE-OR/13_grayscale_overexposure/Level_1/3d1/HTC/',
                  'CURE-OR/15_grayscale_contrast/Level_1/3d1/HTC/',
                  'CURE-OR/16_grayscale_dirtylens1/Level_1/3d1/HTC/',
                  'CURE-OR/18_grayscale_saltpepper/Level_1/3d1/HTC/',
                  'CURE-OR/12_grayscale_underexposure/Level_5/3d1/HTC/',
                  'CURE-OR/13_grayscale_overexposure/Level_5/3d1/HTC/',
                  'CURE-OR/15_grayscale_contrast/Level_5/3d1/HTC/',
                  'CURE-OR/16_grayscale_dirtylens1/Level_5/3d1/HTC/',
                  'CURE-OR/18_grayscale_saltpepper/Level_5/3d1/HTC/',
                  'CURE-TSR/Real_Test/CodecError-1/',
                  'CURE-TSR/Real_Test/CodecError-5/',
                  'CURE-TSR/Real_Test/Darkening-1/',
                  'CURE-TSR/Real_Test/Darkening-5/',
                  'CURE-TSR/Real_Test/DirtyLens-1/',
                  'CURE-TSR/Real_Test/DirtyLens-5/',
                  'CURE-TSR/Real_Test/Exposure-1/',
                  'CURE-TSR/Real_Test/Exposure-5/',
                  'CURE-TSR/Real_Test/GaussianBlur-1/',
                  'CURE-TSR/Real_Test/GaussianBlur-5/',
                  'CURE-TSR/Real_Test/Haze-1/',
                  'CURE-TSR/Real_Test/Haze-5/',
                  'CURE-TSR/Real_Test/LensBlur-1/',
                  'CURE-TSR/Real_Test/LensBlur-5/',
                  'CURE-TSR/Real_Test/Noise-1/',
                  'CURE-TSR/Real_Test/Noise-5/',
                  'CURE-TSR/Real_Test/Rain-1/',
                  'CURE-TSR/Real_Test/Rain-5/',
                  'CURE-TSR/Real_Test/Shadow-1/',
                  'CURE-TSR/Real_Test/Shadow-5/',
                  'CURE-TSR/Real_Test/Snow-1/',
                  'CURE-TSR/Real_Test/Snow-5/',
                  'CURE-TSD/analyze/Scene4/01_04_01_03_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_03_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_04_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_04_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_05_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_05_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_06_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_06_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_07_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_07_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_08_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_08_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_09_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_09_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_10_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_10_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_11_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_11_05/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_12_01/resized/',
                  'CURE-TSD/analyze/Scene4/01_04_01_12_05/resized/',
                  'SIDD/0001_NOISY_SRGB/resized/',
                  'SIDD/0002_NOISY_SRGB/resized/',
                  'SIDD/0003_NOISY_SRGB/resized/',
                  'SIDD/0051_NOISY_SRGB/resized/',
                  'SIDD/0060_NOISY_SRGB/resized/',
                  'SIDD/0080_NOISY_SRGB/resized/',
                  'SIDD/0081_NOISY_SRGB/resized/',
                  'SIDD/0101_NOISY_SRGB/resized/',
                  'SIDD/0125_NOISY_SRGB/resized/',
                  'SIDD/0150_NOISY_SRGB/resized/',
                  'SIDD/0175_NOISY_SRGB/resized/',
                  'Set12/Set12_g15/',
                  'Set12/Set12_g30/',
                  'Set12/Set12_poisson/',
                  'Set12/Set12_saltAndPep/',
                  'Set12/Set12_speckle/'
                  ]

### Initialize filter used in noise PSD estimation
filter = np.array([[1, -2, 1],
                   [-2, 4, -2],
                   [1, -2, 1]])

### Initialize array to hold sigma values for each dataset
sigmas = np.zeros(len(subfolder_list))
ii = 0 # counter for indexing

for data_subfolder in subfolder_list:

    ### Print program start time
    now = datetime.datetime.now()
    print('------')
    print('| Program start time: ')
    print('| ' + now.strftime("%Y-%m-%d %H:%M:%S"))

    ### Load dataset
    ### This code was written to only load one folder of images at a time, as each of the datasets are very large
    ### home_path = base path to get to folder containing all datasets
    home_path      = '/Users/erinshappell/Dropbox (GaTech)/Coursework/Fall 2023/'
    data_path      =  home_path + data_subfolder

    ### Get the names of all the images in the folder
    print('| Dataset path: ' + data_path)
    data_img_names = sorted(glob.glob(data_path + '*jpg'))
    if len(data_img_names) == 0:
        data_img_names = sorted(glob.glob(data_path + '*bmp'))
        if len(data_img_names) == 0:
            data_img_names = sorted(glob.glob(data_path + '*png'))
            if len(data_img_names) == 0:
                data_img_names = sorted(glob.glob(data_path + '*PNG'))

    num_imgs = len(data_img_names)
    print('| Found %d images' % num_imgs)

    ### Load the first noisy image
    img = dip.imread(data_img_names[0])

    ### Convert to grayscale (if necessary)
    if len(img.shape) > 2:
        img = dip.rgb2gray(img)
    img = dip.im_to_float(img)

    ### For the first image ONLY, estimate the noise PSD
    # Code snippet credit: https://stackoverflow.com/questions/2440504/noise-estimation-noise-measurement-in-image
    sigmas[ii] = np.sum(np.sum(np.absolute(dip.convolve2d(img, filter))))
    sigmas[ii] = sigmas[ii] * math.sqrt(0.5 * math.pi) / (6 * (img.shape[0] - 2) * (img.shape[1] - 2))
    if sigmas[ii] == 0:
        print('| Sigma estimated to be 0 (likely in error). Will use 0.2 by default.')
        sigmas[ii] = 0.2
    print('| Sigma = %.5f' % sigmas[ii])

    ii += 1

### Save calculated metrics to csv
sigmas = np.round(sigmas, 5) # truncate to 5 decimal places
metrics = pd.DataFrame(sigmas.T, columns=['sigma'])
metrics.insert(0, 'filename', subfolder_list)
metrics.to_csv(home_path + 'sigmas.csv')

### Print program end time
now = datetime.datetime.now()
print('| Program end time: ')
print('| ' + now.strftime("%Y-%m-%d %H:%M:%S"))
print('------')
