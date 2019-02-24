#=============================================================================#
# Create Cameras Path                                              23.02.2019 #
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
print(timestamp + ' |START| Create Cameras Path')




# Script parameters
elevation = 700 # None | height
kml = 'luzern.kml' # None | KML file example: geoadmin.kml
path2D = None # None | list example: [[2744080, 1234903], [2742223, 1235647]]
pitch = -45 # degree
steps = 2 # meter
root = r'C:\temp'




def wgs84tolv95(coordWGS84):
    url = "http://geodesy.geo.admin.ch/reframe/wgs84tolv95"
    parameter = {"easting": coordWGS84[0],
                 "northing": coordWGS84[1],
                 "format": "json"}
    response = requests.get(url=url, params=parameter)
    result = response.json()
    eLV95 = float(result["easting"])
    nLV95 = float(result["northing"])
    return [eLV95, nLV95]




if kml != None:
    with open(kml, 'r') as fp:
        fileLine = fp.readline()
        if fileLine.find('<coordinates>'):
            coordinates = fileLine.split('<coordinates>')[1].split('</coordinates>')[0]
    path2D = []
    for p in coordinates.split(' '):
        c = p.split(',')
        path2D.append(wgs84tolv95([float(c[0]),float(c[1])]))

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp + ' |INFO | KML interpreted')

else:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp + ' |INFO | path2D interpreted')




# Calculating camera positions in WGS84
url = "http://geodesy.geo.admin.ch/reframe/lv95towgs84"

positions = []
headings = []
elevations = []
pitches = []
mode = 'Path'

offset = 0
for i in range (0, len(path2D)-1):
    dist = offset
    eStart = path2D[i][0]
    nStart = path2D[i][1]
    eEnd = path2D[i+1][0]
    nEnd = path2D[i+1][1]
    azimut = math.atan2((eEnd - eStart), (nEnd - nStart))
    distTotal = math.sqrt((eEnd - eStart)**2 + (nEnd - nStart)**2)

    while dist < distTotal:
        eLV95 = eStart + dist * math.sin(azimut)
        nLV95 = nStart + dist * math.cos(azimut)
        dist += steps

        parameter = {"easting": eLV95,
                     "northing": nLV95,
                     "format": "json"}
        response = requests.get(url=url, params=parameter)
        result = response.json()

        eWGS84 = float(result["easting"])
        nWGS84 = float(result["northing"])

        position = [eWGS84, nWGS84]
        heading = azimut / math.pi * 180 - 180
        if elevation != None:
            elevations.append(elevation)
        else:
            if elevToTerrain != None:
                elevations.append(coord2height([eLV95, nLV95]) + elevToTerrain)

        positions.append(position)
        headings.append(heading)
        pitches.append(pitch)

    offset = dist - distTotal

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
print(timestamp + ' |END  | Create Cameras Path')
