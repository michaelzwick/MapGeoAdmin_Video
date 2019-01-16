#=============================================================================#
# Create Video                                                     10.01.2019 #
#-----------------------------------------------------------------------------#
#                                                                             #
# Michael Zwick | Topografischer Fachspezialist | VBS / swisstopo             #
#                                                                             #
#=============================================================================#

import time
import datetime
from moviepy.editor import *

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(time + ' |START| Create Video')




# Script parameters
root = 'C:\temp'
folder = 'Images'
directory = os.path.join(root, folder)

# Sort images
files = os.listdir(directory)
files = [int(x[:-4]) for x in files]
files = sorted(files, key=int)
files = [str(x)+'.png' for x in files]




# Create list of images and collect to video
images = []
for file in files:
    images.append(os.path.join(directory, file))
clip = ImageSequenceClip(images, fps=24)
clip.write_videofile('movie.mp4') # default codec: 'libx264', 24 fps

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(time + ' |END  | Create Video')
