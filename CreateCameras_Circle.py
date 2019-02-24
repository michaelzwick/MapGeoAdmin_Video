#=============================================================================#
# Create Cameras Circle                                            23.02.2019 #
#-----------------------------------------------------------------------------#
#                                                                             #
# Michael Zwick | Topografischer Fachspezialist | VBS / swisstopo             #
#                                                                             #
#=============================================================================#

import os
import math
import pickle
import datetime
import requests

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |START| Create Cameras Circle')




# Script parameters
center = [2744170, 1234917] # Saentis
elevation = 3500
pitch = -12
radius = 3000
steps = 360
root = r'C:\temp'




# Calculating camera positions in WGS84
url = "http://geodesy.geo.admin.ch/reframe/lv95towgs84"

positions = []
headings = []
elevations = []
pitches = []
mode = 'Circle'

for i in range (0, steps):
    heading = 360.0 / steps * i
    if heading == 0:
        alpha = 0
    else:
        alpha = math.pi/180.0*heading
    eLV95 = center[0] + radius * math.sin(alpha)
    nLV95 = center[1] + radius * math.cos(alpha)

    parameter = {"easting": eLV95,
                 "northing": nLV95,
                 "format": "json"}
    response = requests.get(url=url, params=parameter)
    result = response.json()

    eWGS84 = result["easting"]
    nWGS84 = result["northing"]
    position = [eWGS84, nWGS84]    

    positions.append(position)
    headings.append(heading)
    elevations.append(elevation)
    pitches.append(pitch)
    
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Calculating camera positions done')




# Save the camera parameters in a file
file = open('cameras.pkl', 'wb')
pickle.dump(positions, file)
pickle.dump(headings, file)
pickle.dump(elevations, file)
pickle.dump(pitches, file)
pickle.dump(mode, file)
file.close()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Saveing data done')

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |END  | Create Cameras Circle')