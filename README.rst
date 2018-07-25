SonyPy - Implements the Sony Camera Remote API
==============================================

This Program was first wrtten by Scott Torborg. However, it was designed for Python 2. Now with my modifications it's working with Python 3 on Windows platform. Some regexs are fixed and the binary streams are better handled so the stream_liveview function works. You can show the liveview using cv2, or you can decode the binary stream yourself. Have a try with your sony cameras!!!

Scott Torborg - `Cart Logic <http://www.cartlogic.com>`_

Zander Mao `Email Me If You Have Any Advice ^_^ <mailto:sherlingford@foxmail.com>` 


Installation
============

Install with pip::

    $ pip install sonypy


Quick Start
===========

1. Install ``sonypy``.
2. Enable remote control over Wifi on your camera.
3. Connect your computer to the wifi network hosted by the camera.
4. Open a Python shell.

Now you can start playing::

    >>> from sonypy import Discoverer, Camera

First try to connect to a camera::

    >>> discoverer = Discoverer()
    >>> cameras = discoverer.discover()
    >>> cameras
    [<Camera ...>, <Camera ...>]

Take a shot with current settings::

    >>> cam = cameras[0]
    >>> cam.act_take_picture()


License
=======

SonyPy is licensed under an MIT license. Please see the LICENSE file for more
information.
