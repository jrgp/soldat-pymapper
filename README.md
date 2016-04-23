# Soldat PyMapper

This is an unfinished attempt at making a Soldat map editor in Python + OpenGL.

Currently, viewing/loading maps works except rendering sceneries is a bit bugged. PRs would
be appreciated :)

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
