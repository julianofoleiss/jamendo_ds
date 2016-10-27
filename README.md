# jamendo_ds
This repository contains code to download CC-compliant datasets.

The files are queried from the Jamendo music service. You must use your own jamendo dev client_id. 
You may acquire one at [https://devportal.jamendo.com/](https://devportal.jamendo.com/). 

**cli.py** is a command-line interface to download datasets from Jamendo. You may either download datasets presented in csv 
(following the jamendo_ds format) or query Jamendo for new filelists.

# jamendo_ds format

The jamendo_ds format is used to describe datasets that may be downloaded through **cli.py** using the csv command. It simply consists of csv files with
the following columns: "genre", "song", "artist", "songno", "downloadurl". Each column is separated by a semi-colon ";" and each track is separated by a new-line character "\n". 
All string entries must be enclosed by double-quotes "**"**".

## example jamendo_ds csv file

    genre;song;artist;songno;downloadurl;\n
    "blues";"Stazioni metropolitane ";"Pasqualino Ubaldini";0000;"https://mp3d.jamendo.com/download/track/601020/mp32/"\n
    "blues";"Inertia ";"The TenGooz";0001;"https://mp3d.jamendo.com/download/track/5695/mp32/"\n
    "blues";"Put up a Resistance ";"Crete Boom";0002;"https://mp3d.jamendo.com/download/track/461559/mp32/"
