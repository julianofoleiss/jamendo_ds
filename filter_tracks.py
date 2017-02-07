import codecs
import sys
import os
from pprint import pprint

def filter_tracks(track_list_file, track_filter_file, output_file, max_tracks=200):

    with codecs.open(track_list_file, "r", encoding='utf-8') as f:
        track_list = f.readlines()

    with codecs.open(track_filter_file, "r", encoding='utf-8') as f:
        filter_list = f.readlines()

    output_file = codecs.open(output_file, "w", encoding='utf-8')
    output_file.write(track_list[0])

    track_list.pop(0)
    filter_list.pop(0)

    tld = dict()
    for t in track_list:
        #print t
        td = t.split(";")
        #print td
        tld["%s_%04d" % (td[0], int(td[3]))] = t
    
    tfd = dict()
    for t in filter_list:
        td = t.split(";")
        tfd["%s_%04d" % (td[0], int(td[1]))] = t
    
    #print len(tld.keys())
    #print len(tfd.keys())

    common_tracks = sorted(list(set(tld.keys()).intersection(set(tfd.keys()))))

    print("%d common tracks were found" % len(common_tracks))

    genre = ""
    i = 0
    for k in common_tracks:
        if genre != tld[k].split(";")[0]:
            i = 0
            genre = tld[k].split(";")[0]

        if i >= max_tracks:
            continue
            
        output_file.write(tld[k])
        i+=1

if __name__ == "__main__":

    filter_tracks("max5000.csv", "max5000_st.csv", "jgtzan_200.csv", 200)

