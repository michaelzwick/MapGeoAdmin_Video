#=============================================================================#
# Create Video                                                     24.05.2019 #
#-----------------------------------------------------------------------------#
#                                                                             #
# Michael Zwick | Topografischer Fachspezialist | VBS / swisstopo             #
#                                                                             #
#=============================================================================#

import time
import pickle
import datetime
from moviepy.editor import *

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |START| Create Video')




# Script parameters
fps = 24




# Sort images
files = os.listdir('Images')
files = [int(x[:-4]) for x in files]
files = sorted(files, key=int)
files = [str(x)+'.png' for x in files]




# Loading camera parameters
file = open('cameras.pkl', 'rb')
positions = pickle.load(file)
headings = pickle.load(file)
elevations = pickle.load(file)
pitches = pickle.load(file)
mode = pickle.load(file)
file.close()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Loading data done')




# Create list of images and collect to video
images = []
for file in files:
    images.append('Images/' + file)
clip = ImageSequenceClip(images, fps=fps)
clip.write_videofile('Video_' + mode + '.mp4') # open with VLC player

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |END  | Create Video')
