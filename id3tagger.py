#! python3 filename.py
# Takes a specific path from a command line argument, then iterates through
# every directory looking for audio files. When an audio file is found,
# it is renamed to the format track_number song_title.extension,
# e.g. '01 cool song.mp3'. Any files that don't have a track number are
# displayed after the program runs. Any files that are duplicates are removed,
# then displayed after the end of the program.

import os
import sys
import re
import pprint

from mutagen.easyid3 import EasyID3


extensions = ['mp3', 'wav', 'aac']
no_tracks = []
duplicates = []
m4a_tracks = []


def change_tags(root, file):
    audio = EasyID3(file)

    try:
        # ['tracknumber'] returns list with a string in format
        # 'track/total' i.e. '01/16'
        track = audio['tracknumber'][0].split('/')[0]
            
    except KeyError:
        track = '00'
        no_tracks.append((root, file)) 
    if len(track) == 1:
        track = '0' + track
        
    title = audio['title'][0]

    period_loc = file.rfind('.')
    extension = file[period_loc + 1:]
    new_title = ' '.join([track, title])

    if len(new_title) + 7 > 260: # 260 is max length allowed for Windows files
        last_space = new_title.rfind('.')
        new_title = new_title[:last_space]
        
    new_title = new_title.replace('"', "'")
    new_title = re.sub(r'[\/:*?<>|]', '_', new_title)
    new_title = '.'.join([new_title, extension])

    try:
	    print(new_title)
    except UnicodeEncodeError:
        print("can't be printed")

    if new_title != file:
        try:
            os.rename(file, new_title)
        except FileExistsError:
            duplicates.append((root, file))
            os.remove(root + "\\" + file)
            

def open_folder(path):
    for root, dirs, files in os.walk(path):
        os.chdir(root)
        for file in files:
            period_loc = file.rfind('.')
            extension = file[period_loc + 1:]
            if extension in extensions:
                change_tags(root, file)
            elif extension == 'm4a':
                m4a_tracks.append(root)

                
def main():
    ########
    # TODO
    # fix running script from the command line
    # currently gives UnicodeEncodeError: 'charmap' codec can't encode character
    # '\xfd' in position 7: character maps to <undefined> running in E:\Music\Music
    ########
    
##    if len(sys.argv) == 1:
##        print ("Please enter a path")
##        raise SystemExit
##    else:
##        path = sys.argv[1]
##
##    try:
##        os.chdir(path)
##    except OSError as err:
##        print(err)
##    else:
##        open_folder(path)
    
    open_folder('E:\Music')

    print('Files with no track number:')
    pprint.pprint(no_tracks)
    print('Duplicates:')
    pprint.pprint(duplicates)
    print('M4A Files:')
    pprint.pprint(set(m4a_tracks))


if __name__ == '__main__':
    main()
