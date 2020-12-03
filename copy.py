def formatOk(f):
    return f.endswith('.mp3') or f.endswith('.MP3') or f.endswith('.waf') or f.endswith('.WAF')
    
def getFormat(f):
    if f.endswith('.mp3') or f.endswith('.MP3'):
        return "mp3"
    else:
        return "waf"

import sys
import os
import shutil

sep = os.path.sep

def transformSoundFile(soundFile):
    outFile = soundFile.replace('in' + sep, 'out' + sep, 1)
    # ignore already completed files from earlier runs
    if not os.path.exists(outFile):
        soundFormat = getFormat(soundFile)
        transform(soundFile, outFile, soundFormat, soundFormat)
        return 1
    return 0
 
def copyOtherFile(otherFile):
    outFile = otherFile.replace('in' + sep, 'out' + sep, 1)
    # ignore already completed files from earlier runs
    if not os.path.exists(outFile):
        shutil.copy2(otherFile, outFile)
        return 1
    return 0

#find files and convert them
fobj = open("list.txt")
listOfFiles = [line.rstrip() for line in fobj]
fobj.close()

listOfSoundFiles = [f for f in listOfFiles if (formatOk(f) and not ('432' in f))]
listOfOtherFiles = [f for f in listOfFiles if (('432' in f) or not formatOk(f))]
print('Sound (mp3, wav) files (except 432Hz files): ' + str(listOfSoundFiles))
print('Other files: ' + str(listOfOtherFiles))

listOfOutFiles = [f.replace('in' + sep, 'out' + sep, 1) for f in listOfFiles]

# copy non-MP3 and 432Hz files
count = 0
for otherFile in listOfOtherFiles:
    try:
        outFile = otherFile.replace('in' + sep, 'out' + sep, 1)
        count = count + copyOtherFile(otherFile)
        if count % 100 == 0:
            print('# files copied so far: ' + str(count))
    except KeyboardInterrupt as exitExc:
        outFile = otherFile.replace('in' + sep, 'out' + sep, 1)
        if os.path.exists(outFile):
            os.remove(outFile)
        count = count + copyOtherFile(otherFile)
        print('last copied file: ' + outFile)
        print('Copied ' + str(count) + ' of ' + str(len(listOfOtherFiles)) + ' non-mp3 or 432Hz files.')
        sys.exit(0)
    
print('Copied ' + str(count) + ' of ' + str(len(listOfOtherFiles)) + ' non-mp3 or 432Hz files.')
