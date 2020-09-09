The pitch_transposer python script takes the mp3 files inside the "in" folder and converts them from 440Hz to 432Hz, saving the resulting files into the "out" folder.

## Necessary Libraries

+ pydub (see https://github.com/jiaaro/pydub)
+ mutagen (see https://mutagen.readthedocs.io/en/latest/index.html)

# Licenses of the Libraries

+ mit (see https://github.com/jiaaro/pydub/blob/master/LICENSE)
+ gpl-2.0 (see https://github.com/quodlibet/mutagen/blob/master/COPYING)

# License of this Repository

+ gpl-2.0

## Ignored files

Every file which contains "432" in its path or is not mp3 is just copied and not converted.
