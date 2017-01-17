#!/usr/bin/python

"""
Example: 
  python wallpaper_revolver.py -w "C:/wallpapers/"
"""

import ctypes
import os
import time
import sys
import getopt
import argparse
from PIL import Image
from time import gmtime, strftime


def resize(imagePath, maxh=1500, maxw=1300, method=Image.BICUBIC):
    im = Image.open(imagePath)
    w, h = im.size
    whRatio = float(w)/h

    if w > maxw:
        im = im.resize((maxw, int(float(maxw)/whRatio)), method)
    if im.size[1] > maxh:
        im = im.resize((int(maxh*whRatio), maxh), method)

    return im

# returns all files ending with any of the extensions in <suffices>


def getFilesFromDir(path):
    return [name for name in os.listdir(path) if name.endswith(".jpg")]

# any( [True for suffex in suffices if name.endswith(suffix)] )]


parser = argparse.ArgumentParser(description='Wallpaper revolver arguments.')

parser.add_argument("-w", "--wallPapersPath",
                    help="path to wallpapers [REQUIRED]", type=str,
                    default='.', required=True)
parser.add_argument("-t", "--swapTimeOut",
                    help="the duration of each wallpaper (in minutes)",
                    type=int, default=30, required=False)

sys.stdout.flush()

args = vars(parser.parse_args())

swapTimeOut = args['swapTimeOut']
wallPapersPath = args['wallPapersPath']

sys.stdout.flush()

wallFiles = getFilesFromDir(wallPapersPath)

current_wallpaper = wallPapersPath + "_current_wallpaper_.jpg"

while True:
    for i in range(len(wallFiles)):
        #refetch wallpapers each switch
        wallFiles = getFilesFromDir(wallPapersPath)
        sys.stdout.flush()
        filename = wallPapersPath + wallFiles[i]

        #resize and save current wallpaper
        img = resize(filename)
        print strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        img.save(current_wallpaper, format='JPEG', subsampling=0, quality=100)

        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(
            SPI_SETDESKWALLPAPER, 0, current_wallpaper, 3)

        print " ", filename
        time.sleep(60*swapTimeOut)
