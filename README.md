
# Video from map.geo.admin

Create an animated sequence from www.map.geo.admin.ch with Python. Define the georeference and a few further parameters to produce a lot of screenshots. Collect them together to a video file.

## Getting Started

### Installing Software

For a successful process execution of the script the following software is required:
- [Python 3](https://www.python.org/downloads)
- [Chromedriver](http://chromedriver.chromium.org/downloads)

### Installing Library

Install the following libraries for Python:

```
pip install requests
pip install selenium
pip install moviepy
```

## Running Script

### Edit Parameter

The following main parameters should be adapted to the specific project.

#### Geometry Parameter
The center coordinate  in [EPSG:2056](http://spatialreference.org/ref/epsg/ch1903-lv95/)
```
center = [2744170, 1234917] # Saentis
```
Elevation in meter above sea level.
```
elev = 3000
```
Pitch (inclination) in degree , 0 is horizontal.
```
pitch = -20
```
Radius in meter for the camera positions.
```
radius = 2000
```
Steps (amount) of camera positions or amount of screenshots.
```
steps = 4
```
Seconds of sleeping before taking a screenshot.
```
sleep = 60
```

#### Path Parameter
Root folder for the project.
```
root = r'C:\temp'
```
Folder for the image in the root folder. Create that folder before running the script.
```
folder = 'Images'
```
Path for the chromedriver.
```
DRIVER = r'C:\temp\chromedriver.exe'
```

### CreateScreenshots

 - Calculating camera positions and headings in WGS84
 - Defining base URL (different content in www.map.geo.admin.ch)
 - Link and start chromedriver
 - Generate and save image for every camera position 

### CreateVideo

 - Sort images
 - Create list of images and collect it to a video

## Video


## Author

* **Michael Zwick** | [twitter](https://twitter.com/zwickmichael)


## Acknowledgments

* Inspired by David Oesch [GitHub](https://github.com/davidoesch)
* Map viewer of the Federal spatial data infrastructure (FSDI) [map.geo.admin.ch](https://github.com/davidoesch)
* Data from the Federal Office of Topography [swisstopo](https://swisstopo.ch)
