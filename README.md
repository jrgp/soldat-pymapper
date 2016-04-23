# Soldat PyMapper

This is an unfinished Soldat map editor written in Python + OpenGL. I'm releasing
this in its unfinished state as maybe someone will find the binary map parsing code
helpful. (See the pms/ folder)

Viewing/loading maps works except rendering sceneries is a bit bugged. PRs would
be appreciated :)

Use the scroll wheel to zoom in/out and wasd keys to move around.

Example rendering of a map rendering the background gradient, textures, and polygons:
![Octopus](http://jrgp.us/screenshots/pymapper_8.png)

Just show the polygons in wireframe format:
![Octopus wireframe](http://jrgp.us/screenshots/pymapper_9.png)

### Install dependencies

On mac:

    brew install pyqt qt
    sudo pip install PyOpenGL Pillow

On Ubuntu/Debian:

    apt-get install python-qt4 python-qt4-gl python-opengl python

### Run it

On mac:

    PYTHONPATH=/usr/local/lib/python2.7/site-packages/ python pymapper.py

On Linux:

    python pymapper.py
