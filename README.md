# ECE 6258 Project Fall 2023
This repository contains code written or modified for a project titled "An objective comparison and analysis of the performance of the BM3D and DnCNN image processing algorithms on denoising." See below for a brief description of each file:

## Code
### BM3D
- **bm3d_process.py** -- Python script used to run BM3D on a folder of images
- **save_sigmas.py** -- Python script used to save estimates of noise PSD used in BM3D analysis
- **violinplot.py** -- Python script used to produce a violin distribution plot for the noise PSD values used in BM3D analysis
- **resize_imgs.m** -- MATLAB script to resize a folder of images using MATLAB's built-in *imresize* method
### DnCNN
- **DnCNN_block.m** -- MATLAB script to run DnCNN on a folder of images using block processing
- **DnCNN_OR.m** -- MATLAB script to run DnCNN on the CURE-OR dataset
- **DnCNN_SIDD.m** -- MATLAB script to run DnCNN on the SIDD dataset
### IQA
- **cw_ssim.py** -- Python script to process a folder of images using the CW-SSIM metric
- **runCSV.m** -- MATLAB script to process a folder of images using the CSV metric
- **runMSUNIQUE.m** -- MATLAB script to process a folder of images using the MS-UNIQUE metric
- **runSUMMER.m** -- MATLAB script to process a folder of images using the SUMMER metric
- **runUNIQUE.m** -- MATLAB script to process a folder of images using the UNIQUE metric

