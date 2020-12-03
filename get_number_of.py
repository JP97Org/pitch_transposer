import sys
import os
import shutil
from shutil import copy2

sep = os.path.sep

def formatOk(f):
    return f.endswith('.mp3') or f.endswith('.MP3') or f.endswith('.waf') or f.endswith('.WAF')
    
def getFormat(f):
    if f.endswith('.mp3') or f.endswith('.MP3'):
        return "mp3"
    else:
        return "waf"

#find files and convert them
fobj = open("list.txt")
listOfFiles = [line.rstrip() for line in fobj]
fobj.close()

listOfSoundFiles = [f for f in listOfFiles if (formatOk(f) and not ('432' in f))]
listOfOtherFiles = [f for f in listOfFiles if (('432' in f) or not formatOk(f))]
print('Sound (mp3, wav) files (except 432Hz files): ' + str(listOfSoundFiles))
print('Other files: ' + str(listOfOtherFiles))

#TODO adapt listnr
listnr = 24588
mp3Number = -1
for i in range(len(listOfSoundFiles)):
    if listOfSoundFiles[i] == listOfFiles[listnr]:
        mp3Number = i
        break
print('Number of ' + str(listnr) + ' is ' + str(mp3Number))
