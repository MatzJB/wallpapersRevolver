#!/usr/bin/python

"""
Example: python wallpapersRevolver.py -w "C:/wallpapers/" -t 5
"""

from time import gmtime, strftime
from PIL import Image
import argparse
import getopt
import ctypes
import time
import os
import sys


def resize(imagePath, maxh=1500, maxw=1300, method=Image.BICUBIC):
    ''' resize image using default dimensions '''
    im = Image.open(imagePath)
    w, h = im.size
    whRatio = float(w)/h

    if w > maxw:
        im = im.resize((maxw, int(float(maxw)/whRatio)), method)
    if im.size[1] > maxh:
        im = im.resize((int(maxh*whRatio), maxh), method)

    return im


def getFilesFromDir(path):
    ''' returns all files ending with any of the extensions in <suffices>'''
    return [name for name in os.listdir(path) if name.endswith(".jpg")]


def main():

    parser = argparse.ArgumentParser(
        description='Wallpaper revolver arguments.')

    parser.add_argument("-w", "--wallPapersPath",
                        help="path to wallpapers [REQUIRED]", type=str,
                        default='.', required=True)
    parser.add_argument("-t", "--swapTimeOut",
                        help="the duration of each wallpaper (in minutes)",
                        type=int, default=30, required=False)

    parser.add_argument("-v", "--verbosePrints",
                        help="verbose output",
                        action='store_true', required=False)

    args = vars(parser.parse_args())
    swapTimeOut = args['swapTimeOut']
    wallPapersPath = args['wallPapersPath']
    verboseOutput = args['verbosePrints']

    wallFiles = getFilesFromDir(wallPapersPath)

    current_wallpaper = wallPapersPath + "_current_wallpaper_.jpg"

    while True:
        4
        for i in range(len(wallFiles)):
            # refetch wallpapers for each switch in case they are deleted (or
            # use try/exception)
            wallFiles = getFilesFromDir(wallPapersPath)
            sys.stdout.flush()
            filename = wallPapersPath + wallFiles[i]

            # save resized wallpaper in the dir for display
            img = resize(filename)
            if verboseOutput:
                print strftime("%a, %d %b %Y %H:%M:%S", gmtime())
            img.save(
                current_wallpaper, format='JPEG', subsampling=0, quality=100)

            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoA(
                SPI_SETDESKWALLPAPER, 0, current_wallpaper, 3)

            if verboseOutput:
                print " ", filename
            time.sleep(60*swapTimeOut)


if __name__ == '__main__':
    main()
