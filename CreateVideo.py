#=============================================================================#
# Create Video                                                     23.02.2019 #
#-----------------------------------------------------------------------------#
#                                                                             #
# Michael Zwick | Topografischer Fachspezialist | VBS / swisstopo             #
#                                                                             #
#=============================================================================#

import time
import pickle
import datetime
from moviepy.editor import *

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(time + ' |START| Create Video')




# Script parameters
root = r'C:\temp'
folder = 'Images'
directory = os.path.join(root, folder)




# Sort images
files = os.listdir(directory)
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
    images.append(os.path.join(directory, file))
clip = ImageSequenceClip(images, fps=24)
clip.write_videofile('Video_' + mode + '.mp4') # open with VLC player

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Video creating done')

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(time + ' |END  | Create Video')
