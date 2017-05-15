#!/usr/bin/python3
# Filename: GetBingBackgroundImage.py
# coding=utf-8

import sys
import urllib.request

import re
import os
import shutil
from threading import Timer

imageDir = "./images/"
bakDir = "./baks/"
#url = "http://global.bing.com/?FORM=HPCNEN&setmkt=en-us&setlang=en-us"
URL = "http://cn.bing.com/"
wallpaperFileName = "1.jpg"

def getHtml(url):
    # page = urllib.urlopen(url)
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


def getImg(html):
    reg = r'g_img={url: "(.+\.jpg)"'
    pageCode = html.decode()
    match = re.search(reg, pageCode)
    imgList = ()
    if (match != None):
        imgList = match.groups()
    return imgList


def saveImg(imgList):
    if len(imgList) > 0:
        imgUrl = imgList[0]
        reg = r'[\w-]+\.jpg'
        fileNameRe = re.compile(reg)
        fileNameList = re.findall(fileNameRe, imgUrl)
        imgUrl = URL + imgUrl
        if len(fileNameList) > 0:
            fileName = fileNameList[0]

            if not os.path.isdir(bakDir):
                os.mkdir(bakDir)

            if not os.path.isdir(imageDir):
                os.mkdir(imageDir)

            if not os.path.isfile(bakDir + fileName):
                urllib.request.urlretrieve(imgUrl, bakDir + fileName)
                os.remove(imageDir + wallpaperFileName);

            if not os.path.isfile(imageDir + wallpaperFileName):
                os.symlink(os.path.abspath(bakDir) + "/" + fileName, imageDir + wallpaperFileName)


            # if not os.path.isfile(bakDir + fileName):
            #     if os.path.isdir(imageDir):
            #         if not os.path.isdir(bakDir):
            #             os.mkdir(bakDir)
            #         # moveDir(imageDir, bakDir)
            #
            #     else:
            #         os.mkdir(imageDir)
            #     urllib.request.urlretrieve(imgUrl, imageDir + fileName)


def moveDir(src, des):
    fileList = os.listdir(src);
    for childFileName in fileList:
        shutil.move(src + childFileName, des)

def get(url):
    html = getHtml(url)
    imgList = getImg(html)
    print(imgList)
    saveImg(imgList)


sourcefile_url = sys.argv[0]
sourcefile_url = sourcefile_url.replace("GetBingBackgroundImage.py", "")
os.chdir(sourcefile_url)
get(URL)

while True:
    Timer(600, get, (URL,)).run()
