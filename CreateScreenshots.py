#=============================================================================#
# Create Screenshots                                               24.05.2019 #
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
window = 'iFrame' # 'Standard' | 'iFrame' | 'Mobile'
sleep = 60
start = 206
baseUrl = 'https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=ch.swisstopo.pixelkarte-farbe&layers=ch.swisstopo.swissnames3d'
path = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists('Images'):
    os.makedirs('Images')




# Loading camera parameters
file = open('cameras.pkl', 'rb')
positions = pickle.load(file)
headings = pickle.load(file)
elevations = pickle.load(file)
pitches = pickle.load(file)
file.close()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |INFO | Loading data done')




# Create iFrame
iframe = 'iframe.html'
def url2iframe(mainurl, iframe):
    file = open(iframe,'w')
    file.write("<iframe src='https://map.geo.admin.ch/embed.html?")
    file.write(mainurl.split("map.geo.admin.ch/")[1] + "' ")
    file.write("width='100%' height='95%' frameborder='0' style='border:0'/>'")
    file.close()




# Link and start chromedriver
# Source: http://chromedriver.chromium.org/downloads
DRIVER = 'chromedriver.exe'
driver = webdriver.Chrome(DRIVER)
driver.set_window_size(1920, 1200)




# Generate and save image for every camera position
for i in range (0,len(positions)):
    if i >= start-1:
        mainurl = baseUrl + '&lon=' + str(positions[i][0]) + '&lat=' + str(positions[i][1]) + '&elevation=' + str(elevations[i]) + '&heading=' + str(headings[i]) + '&pitch=' + str(pitches[i])
        if window == 'Standard':
            driver.get(mainurl)
        elif window == 'iFrame':
            url2iframe(mainurl, iframe)
            driver.get(path + '/' + iframe)
            os.remove(iframe)
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(timestamp + ' |ERROR| No valid window is given')
            exit()
        time.sleep(sleep)
        driver.save_screenshot('Images/' + str(i+1) + '.png')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp + ' |INFO | Screenshot ' + str(i+1) + '/' + str(len(positions)) + ' done')
driver.quit()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp + ' |END  | Create Screenshots')
