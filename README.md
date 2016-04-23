# Soldat PyMapper

This is an unfinished Soldat map editor written in Python + OpenGL. I'm releasing
this in its unfinished state as I'm happy with my binary map parsing code.

Viewing/loading maps works except rendering sceneries is a bit bugged. PRs would
be appreciated :)

![Octopus](http://jrgp.us/screenshots/pymapper_8.png)
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
