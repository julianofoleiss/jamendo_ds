# -*- coding: utf-8 -*-

import codecs
import os

def rename_files(directory, rename_file, rename_offset, extension):

    with codecs.open(rename_file, "r", encoding='utf-8') as f:
        track_list = f.readlines()

    tracks = [ i.strip().split(";") for i in track_list ]
    
    for t in tracks:
        try:
            if t[0] == 'x' or t[0] == '?':
                filename = "%s%s_%04d.%s" % (directory, t[1], int(t[2]), extension)
                print "deleting %s ..." % filename
                os.unlink(filename)
            
            if t[0] == 'r':
                org_name = "%s%s_%04d.%s" % (directory, t[1], int(t[2]), extension)
                new_name = "%s%s_%04d.%s" % (directory, t[3], int(t[2]) + rename_offset, extension)
                print "renaming %s to %s ..." % (org_name, new_name) 
                os.rename(org_name, new_name)

        except OSError as err:
            if(err.errno == 2):
                print("file not found. continuing...")


if __name__ == "__main__":
    
    directory = "jgtzan_200/"
    rename_file = "rename.csv"
    rename_offset = 2000
    extension = "mp3"

    rename_files(directory, rename_file, rename_offset, extension)

    

