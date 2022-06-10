import os
from unipath import Path
import time
start = time.time()

'''This program creates a second folder as [folder_name]_corrected 
    and corrects all the headers from broken .wav files
            it just needs the path'''
# __________________________________________________________________________

path_to_files = r'C:\Users\Jonas Bousquet\Desktop\pyhy3\Data\DW backup'

# __________________________________________________________________________


newHeader = b'RIFF$\xfe\xdf\x06WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00w\x01\x00\x00\xee\x02\x00\x02\x00\x10\x00data\x00\xfe\xdf\x06'
p = Path(path_to_files)
new = str(p.name)+'_corrected'
corrected = Path(p.parent, new)
corrected.mkdir()

for filename in os.listdir(path_to_files):
    file = path_to_files + '/' + filename
    newfile = str(corrected) + '/'+ filename
    with open(f'{file}', 'rb') as f:
        binaryHeader = f.read(44)
        binarySound = f.read()
        with open(f'{newfile}', 'wb') as out:
            out.write(newHeader)
            out.write(binarySound)

end = time.time()
zeit = end - start
if zeit > 60:
    minutes = int(zeit / 60)
    sec = zeit % 60
    sec = round(sec, 2)
    print(f'\nscript run in {minutes} m and {sec} s')
else:
    zeit = round(zeit, 2)
    print(f'\nscript run in {zeit} s')