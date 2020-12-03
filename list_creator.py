def formatOk(f):
    return f.endswith('.mp3') or f.endswith('.MP3') or f.endswith('.waf') or f.endswith('.WAF')
    
def getFormat(f):
    if f.endswith('.mp3') or f.endswith('.MP3'):
        return "mp3"
    else:
        return "waf"

import sys
import os

sep = os.path.sep

#find files and convert them
listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk('in' + sep):
    #print(dirpath)
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

for filepath in listOfFiles:
    print(filepath)
