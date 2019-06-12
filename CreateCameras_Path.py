#=============================================================================#
# Create Cameras Path                                              24.05.2019 #
#-----------------------------------------------------------------------------#
#                                                                             #
# Michael Zwick | Topografischer Fachspezialist | VBS / swisstopo             #
#                                                                             #
#=============================================================================#

import os
import ast
import math
import time
import pickle
import datetime
import requests

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |START| Create Cameras Path')




# Script parameters
kml = 'line.kml' # None | KML file example: geoadmin.kml
path2D = None # None | list example: [[2600334, 1199351],[2600276, 1199419]] # Marzilibahn
elevation = 700 # None | height
pitch = -20 # degree
step = 2 # meter
iteration = 3

def string2list(string):
    listNew = []
    stringNew = string.split('[[')[1].split(']]')[0].split('],[')
    for i in range(0,len(stringNew)):
        e = float(stringNew[i].split(',')[0])
        n = float(stringNew[i].split(',')[1])
        listNew.append([e, n])
    return listNew

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

def lv95towgs84(coordLV95):
    url = "http://geodesy.geo.admin.ch/reframe/lv95towgs84"
    parameter = {"easting": coordLV95[0],
                 "northing": coordLV95[1],
                 "format": "json"}
    response = requests.get(url=url, params=parameter)
    result = response.json()
    eWGS84 = float(result["easting"])
    nWGS84 = float(result["northing"])
    return [eWGS84, nWGS84]

def getDist(point1, point2):
    dist = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
    return dist

def getAzi(point1, point2):
    azi = math.atan2((point2[0]-point1[0]), (point2[1]-point1[1]))
    return azi

def calcPolar(point, azi, dist):
    point2 = [point[0] + dist * math.sin(azi), point[1] + dist * math.cos(azi)] 
    return point2

def list2linekml(coordList, CRS):
    f = open('path.kml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><Placemark><LineString><coordinates>')
    if CRS == 'WGS84':
        for i in range(0,len(coordList)):
            f.write(str(coordList[i][0]) + ',' + str(coordList[i][1]) + ' ')
    elif CRS == 'LV95':
        for i in range(0,len(coordList)):
            WGS84 = lv95towgs84([coordList[i][0], coordList[i][1]])
            f.write(str(WGS84[0]) + ',' + str(WGS84[1]) + ' ')
    else:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp + ' |ERROR| No valid CRS is given')
        exit()
    f.write('</coordinates></LineString></Placemark></Document></kml>')
    f.close()

def list2pointskml(coordList, CRS):
    f = open('points.kml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>')
    if CRS == 'WGS84':
        for i in range(0,len(coordList)):
            f.write('<Placemark><Point><coordinates>')
            f.write(str(coordList[i][0]) + ',' + str(coordList[i][1]))
            f.write('</coordinates></Point></Placemark>')
    elif CRS == 'LV95':
        for i in range(0,len(coordList)):
            f.write('<Placemark><Point><coordinates>')
            WGS84 = lv95towgs84([coordList[i][0], coordList[i][1]])
            f.write(str(WGS84[0]) + ',' + str(WGS84[1]))
            f.write('</coordinates></Point></Placemark>')
    else:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp + ' |ERROR| No valid CRS is given')
        exit()
    f.write('</Placemark></Document></kml>')
    f.close()

def path2curve(path2D):
    path2Dnew = []
    path2Dnew.append(path2D[0])
    for i in range(1,len(path2D)-1):
        p1 = path2D[i-1]
        p2 = path2D[i]
        p3 = path2D[i+1]
        d1 = getDist(p1,p2)
        d2 = getDist(p2,p3)
        a1 = getAzi(p2,p1)
        a2 = getAzi(p2,p3)
        if d1 <= d2:
            d = d1
        else:
            d = d2
        path2Dnew.append(calcPolar(p2,a1,d/4.0))
        path2Dnew.append(calcPolar(p2,a2,d/4.0))
    path2Dnew.append(path2D[-1])
    return path2Dnew

def dirInterpol(headings):
    headingLast = None
    headingGroup = []
    headingAmount = []
    for heading in headings:
        if headingLast != heading:
            headingLast = heading
            headingGroup.append(heading)
            count = 1
            headingAmount.append(count)
        else:
            count += 1
            headingAmount[-1] = count

    for i in range(0, len(headingGroup)):
        if i > 0:
            l1 = headingGroup[i-1]
            l2 = headingGroup[i]
            if abs(l1-l2) > 180:
                if l1 < l2:
                    headingGroup[i] = l2-360
                elif l1 < l2:
                    headingGroup[i] = l2+360
            
    headings = []
    lenInterpolLast = 0
    for i in range(0, len(headingGroup)):
        if i < len(headingGroup)-1:
            l1 = headingAmount[i]
            l2 = headingAmount[i+1]
            if l1 <= l2:
                lenInterpol = int(l1/2)
            else:
                lenInterpol = int(l2/2)
            if lenInterpol != 0:
                stepInterpol = (headingGroup[i+1]-headingGroup[i])/(lenInterpol*2+1)
            else:
                stepInterpol = 0
            for j in range (lenInterpolLast, headingAmount[i]-lenInterpol):
                headings.append(headingGroup[i])
            for k in range (0, lenInterpol * 2):
                headings.append(headingGroup[i] + (k+1) * stepInterpol)
                lenInterpolLast = lenInterpol
        else:
            for l in range (0, headingAmount[i]-lenInterpol):
                headings.append(headingGroup[-1])
    return headings




# Loading path
if kml != None:
    with open(kml, 'r') as fp:
        fileLine = fp.readline()
        if fileLine.find('<coordinates>'):
            try:
                coordinates = fileLine.split('<coordinates>')[1].split('</coordinates>')[0]
            except:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(timestamp + ' |ERROR| Wrong KML. Digitize on www.map.geo.admin.ch.')
    path2D = []
    for p in coordinates.split(' '):
        c = p.split(',')
        path2D.append(wgs84tolv95([float(c[0]),float(c[1])]))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp + ' |INFO | KML interpreted')
else:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp + ' |INFO | Path2D interpreted')




# Smoothing path
for i in range(0,iteration):
    path2D = path2curve(path2D)
list2linekml(path2D, 'LV95')

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Smoothing path done')




# Calculating camera positions in WGS84
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
        dist += step
        position = lv95towgs84([eLV95, nLV95])
        heading = azimut / math.pi * 180
        if elevation != None:
            elevations.append(elevation)
        else:
            if elevToTerrain != None:
                elevations.append(coord2height([eLV95, nLV95]) + elevToTerrain)

        positions.append(position)
        if heading < 0:
            headings.append(heading+360.0)
        else:
            headings.append(heading)
        pitches.append(pitch)

    offset = dist - distTotal

headings = dirInterpol(headings)
list2pointskml(positions, 'WGS84')
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Calculating ' + str(len(headings)) + ' camera positions done')




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
