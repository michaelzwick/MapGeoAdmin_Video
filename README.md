# Video from map.geo.admin
Create an animated sequence from www.map.geo.admin.ch with Python. Create a list of camera positions for a Circle, Round or Path. Produce a screenshots for every camera position. Collect them together to a video file.

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

## Running Scripts
- CreateCameras (choose one mode)
  - Circle
  - Path
  - Round
- CreateScreenshots
- CreateVideo

### [CreateCameras_Circle.py](CreateCameras_Circle.py)
- Using center coordinate and radius
- Calculating camera positions in WGS84, elevations, headings and pitches
- Save calculations in a dump file
![Image Circle](https://github.com/michaelzwick/MapGeoAdmin_Video/Mode_Circle.png "Circle")

### [CreateCameras_Path.py](CreateCameras_Path.py)
- Using path in list format or KML file
- Calculating camera positions in WGS84, elevations, headings and pitches
- Save calculations in a dump file
![Image Path](https://github.com/michaelzwick/MapGeoAdmin_Video/Mode_Path.png "Path")

### [CreateCameras_Round.py](CreateCameras_Round.py)
- Using center coordinate
- Calculating camera positions in WGS84, elevations, headings and pitches
- Save calculations in a dump file
![Image Round](https://github.com/michaelzwick/MapGeoAdmin_Video/Mode_Round.png "Round")

### [CreateScreenshots.py](CreateScreenshots.py)
- Defining base URL from www.map.geo.admin.ch
- Link and start chromedriver
- Generate and save image for every camera position 

### [CreateVideo.py](CreateVideo.py)
- Sort images
- Create list of images and collect them to a video
- Save the MP4 video file

## Edit Parameter
The following main parameters should be adapted to the specific project.

### Geometry Parameter
Coordinates  in [EPSG:2056](http://spatialreference.org/ref/epsg/ch1903-lv95/)
```
center = [2744170, 1234917] # Saentis
path2D = [[2693518, 1203751], [2693925, 1205214]] # Stoosbahn
```
KML file with one `LineString` in [EPSG:4326](http://spatialreference.org/ref/epsg/wgs-84/) in example from [map.geo.admin.ch](https://map.geo.admin.ch)
```
kml = 'luzern.kml'
```
Constant elevation in meter above sea level.
```
elevation = 3000
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

## Video
[Video_Saentis.mp4](Video_Saentis.mp4)
[Video_Luzern.mp4](Video_Luzern.mp4)
[Video_Gurten.mp4](Video_Gurten.mp4)
Open with [VLC](https://www.videolan.org) player

## Author
* **Michael Zwick** | [twitter](https://twitter.com/zwickmichael)


## Acknowledgments
* Inspired by David Oesch [GitHub](https://github.com/davidoesch)
* Map viewer of the Federal spatial data infrastructure (FSDI) [map.geo.admin.ch](https://map.geo.admin.ch)
* Data from the Federal Office of Topography [swisstopo](https://swisstopo.ch)