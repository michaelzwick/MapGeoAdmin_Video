#=============================================================================#
# Create Screenshots                                               16.02.2019 #
#-----------------------------------------------------------------------------#
#                                                                             #
# Michael Zwick | Topografischer Fachspezialist | VBS / swisstopo             #
#                                                                             #
#=============================================================================#

import os
import math
import time
import pickle
import datetime
import requests
from selenium import webdriver

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |START| Create Screenshots')




# Script parameters
sleep = 60
root = r'C:\temp'
folder = 'Images'
start = 1

directory = os.path.join(root, folder)
if not os.path.exists(directory):
    os.makedirs(directory)




# Loading camera parameters
file = open('cameras.pkl', 'rb')
positions = pickle.load(file)
headings = pickle.load(file)
elevations = pickle.load(file)
pitches = pickle.load(file)
file.close()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Loading data done')



#baseurl = 'https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=voidLayer&layers=ch.swisstopo.swissimage-product&layers_timestamp=current'
baseurl = 'https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=ch.swisstopo.pixelkarte-farbe&layers=ch.swisstopo.swissnames3d'





# Link and start chromedriver
# Source: http://chromedriver.chromium.org/downloads
DRIVER = r'c:\temp\chromedriver.exe'
driver = webdriver.Chrome(DRIVER)
driver.set_window_size(1920, 1200)




# Generate and save image for every camera position
for i in range (0,len(positions)):
    if i >= start-1:
        mainurl = baseurl + '&lon=' + str(positions[i][0]) + '&lat=' + str(positions[i][1]) + '&elevation=' + str(elevations[i]) + '&heading=' + str(headings[i]-180) + '&pitch=' + str(pitches[i])
        driver.get(mainurl)
        time.sleep(sleep)
        driver.save_screenshot(os.path.join (directory, str(i+1) + '.png'))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp + ' |INFO | Screenshot ' + str(i+1) + '/' + str(len(positions)) + ' done')
driver.quit()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |END  | Create Screenshots')
