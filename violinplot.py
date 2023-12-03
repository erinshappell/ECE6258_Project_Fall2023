#################################################################################
### Violin Plotter
### Code written by Erin Shappell, for ECE 6258 Final Project
### Project Partner: Robert Pritchard
### The purpose of this script is to calculate and save the value of sigma used
### for each BM3D processing session
#################################################################################

### Import libraries
import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
from matplotlib import style

### Load data
home_path = '/Users/erinshappell/Dropbox (GaTech)/Coursework/Fall 2023/'
df        = pd.read_csv(home_path + 'sigmas.csv')

### Create violin plot with matplotlib
plt.style.use('Solarize_Light2')
fig, axes = plt.subplots()

axes.violinplot(dataset = [df[df.Dataset == 'CURE-OR']["Noise PSD"].values,
                           df[df.Dataset == 'CURE-TSR']["Noise PSD"].values,
                           df[df.Dataset == 'CURE-TSD']["Noise PSD"].values,
                           df[df.Dataset == 'SIDD']["Noise PSD"].values,
                           df[df.Dataset == 'Set12']["Noise PSD"].values ] )

axes.yaxis.grid(True)
x_labels = ['CURE-OR','CURE-TSR','CURE-TSD','SIDD','Set12']
x_ticks = np.arange(1,len(x_labels)+1)
plt.xticks(x_ticks, x_labels)
axes.set_xlabel('Dataset')
axes.set_ylabel('Noise PSD')

plt.show()
