# Watt'n Sound
Code to work with Hydrophone data using Python 3.9

## How to use
This repository is supposed to be used with [Lifewatch pypam[(https://github.com/lifewatch/pypam)

To use data from the Aural you need to prepare the data using **data_correct.py**
**data_correct.py** will go through the folders listed in **deployment_list.txt**, correct all the .wav headers, rename the files from _time_date_name_ to _date_time_name_ and delete the first and last 3 files from each folder to remove the boatnoises used to deplay the hydrophone

To create a comparative spiderplot use **radarchartv7.py**. You will have to specify the path to the **.nc** files you want to compare (works with 2 files right now)
The **.nc** are created using pypams **acoustic_dataset.py** 
<sub> Note: pypam doesn't accept the Aurals filenamestructure right now so time-related anaylsis (e.g. spectrograms) cannot be used </sub>

