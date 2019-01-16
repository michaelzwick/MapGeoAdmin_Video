#=============================================================================#
# Create Screenshots                                               10.01.2019 #
#-----------------------------------------------------------------------------#
#                                                                             #
# Michael Zwick | Topografischer Fachspezialist | VBS / swisstopo             #
#                                                                             #
#=============================================================================#

import os
import math
import time
import datetime
import requests
from selenium import webdriver

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |START| Create Screenshots')




# Script parameters
center = [2617049, 1091670] # Matterhorn
center = [2643435, 1158638] # Eiger
center = [2642836, 1156509] # Moench
center = [2744170, 1234917] # Saentis
elev = 3000
pitch = -20
radius = 2000
steps = 4
sleep = 60
root = r'C:\temp'
folder = 'Images'

directory = os.path.join(root, folder)
points= []
headings = []




# Calculating camera positions and headings in WGS84
url = "http://geodesy.geo.admin.ch/reframe/lv95towgs84"
for i in range (0, steps):
    heading = 360.0 / steps * i
    headings.append(heading)
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
    
    point = [eWGS84, nWGS84]    
    points.append(point)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Calculation done')




#baseurl = 'https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=voidLayer&layers=ch.swisstopo.swissimage-product&layers_timestamp=current'
baseurl = 'https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=ch.swisstopo.pixelkarte-farbe&layers=ch.swisstopo.swissnames3d'

# Link and start chromedriver
# Source: http://chromedriver.chromium.org/downloads
DRIVER = r'C:\temp\chromedriver.exe'
driver = webdriver.Chrome(DRIVER)
driver.set_window_size(1920, 1200)

# Generate and save image for every camera position 
str(points[i][0])
for i in range (0,len(headings)):
    mainurl = baseurl + '&lon=' + str(points[i][0]) + '&lat=' + str(points[i][1]) + '&elevation=' + str(elev) + '&heading=' + str(headings[i]-180) + '&pitch=' + str(pitch)
    driver.get(mainurl)
    time.sleep(sleep)
    driver.save_screenshot(os.path.join (directory, str(i+1) + '.png'))
    print (str(i+1) + '/' + str(steps))
driver.quit()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |END  | Edit Video')
