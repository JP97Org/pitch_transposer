# needed libraries: pydub and mutagen
from pydub import AudioSegment # see https://github.com/jiaaro/pydub
from pydub.playback import play
from mutagen.easyid3 import EasyID3 # see https://mutagen.readthedocs.io/en/latest/index.html

def transform(in_file, out_file, in_format, out_format):
    # see https://stackoverflow.com/questions/43963982/python-change-pitch-of-wav-file
    sound = AudioSegment.from_file(in_file, format=in_format)
    print('Read "' + in_file + '" in 440Hz.')

    x = 0.3177 # x is solution of equation 440 * 2 ^ (- (x/12)) = 432, so that 440 Hz is shifted to 432 Hz
    octaves = - (x / 12.0)

    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

    # keep the same samples but tell the computer they ought to be played at the 
    # new, lower sample rate.
    hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    # now we just convert it to a common sample rate (44.1k - standard audio CD) to 
    # make sure it works in regular audio players.
    hipitch_sound = hipitch_sound.set_frame_rate(44100)

    #Play pitch changed sound
    #play(hipitch_sound) # enable this line in order to play created sound

    #export / save pitch changed sound
    hipitch_sound.export(out_file, format=out_format)
    
    if in_format in "mp3" and out_format in "mp3":
        #copy meta-data
        audio_in = EasyID3(in_file)
        print(audio_in)
        audio_out = EasyID3(out_file)
        for key in audio_in:
            audio_out[key] = audio_in[key]
        if audio_out:
            audio_out.save()
    
    print('Wrote "' + out_file + '" in 432Hz.')

def formatOk(f):
    return f.endswith('.mp3') or f.endswith('.MP3') or f.endswith('.waf') or f.endswith('.WAF')
    
def getFormat(f):
    if f.endswith('.mp3') or f.endswith('.MP3'):
        return "mp3"
    else:
        return "waf"

import os
import shutil
from shutil import copy2

sep = os.path.sep

#find files and convert them
listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk('in' + sep):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

listOfSoundFiles = [f for f in listOfFiles if (formatOk(f) and not ('432' in f))]
listOfOtherFiles = [f for f in listOfFiles if (('432' in f) or not formatOk(f))]
print('Sound (mp3, wav) files (except 432Hz files): ' + str(listOfSoundFiles))
print('Other files: ' + str(listOfOtherFiles))

# creating necessary directories
listOfOutFiles = [f.replace('in' + sep, 'out' + sep, 1) for f in listOfFiles]
for filename in listOfOutFiles:
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

# transform files
count = 0
for soundFile in listOfSoundFiles:
    outFile = soundFile.replace('in' + sep, 'out' + sep, 1)
    # ignore already completed files from earlier runs
    if not os.path.exists(outFile):
        soundFormat = getFormat(soundFile)
        transform(soundFile, outFile, soundFormat, soundFormat)
        count = count + 1
        
print('Transformed ' + str(count) + ' of ' + str(len(listOfSoundFiles)) + ' sound files from 440Hz to 432Hz.')

# copy non-MP3 and 432Hz files
count = 0
for otherFile in listOfOtherFiles:
    outFile = otherFile.replace('in' + sep, 'out' + sep, 1)
    # ignore already completed files from earlier runs
    if not os.path.exists(outFile):
        shutil.copy2(otherFile, outFile)
        count = count + 1
    
print('Copied ' + str(count) + ' of ' + str(len(listOfOtherFiles)) + ' non-mp3 or 432Hz files.')
