# -*- coding: utf-8 -*-

import codecs
import os
import random

if __name__ == "__main__":

    csv_file = "jgtzan_200.csv"
    rename_file = "rename.csv"
    output_filename = "jgtzan.csv"
    max_tracks = 100

    with codecs.open(csv_file, "r", encoding='utf-8') as f:
        csv = f.readlines()

    csv = csv[1:]

    csv_tracks = dict()

    output = []

    #load csv in a dictionary indexed by genre_trackid
    for t in csv:
        d = t.strip().split(";")
        csv_tracks["%s_%04d" % (d[0].replace("\"", ""), int(d[3]))] = ( d[0].replace("\"", "") , d[1], d[2], d[3], d[4], d[5])

    print len(csv_tracks.keys())

    #load rename file in a list
    with codecs.open(rename_file, "r", encoding='utf-8') as f:
        rename_list = f.readlines()

    rename_tracks = [ i.strip().split(";") for i in rename_list ]

    rename_tracks = rename_tracks[1:]

    count = {
        'blues': 2000,
        'classical': 2000,
        'country': 2000,
        'disco': 2000,
        'hiphop' : 2000,
        'jazz' : 2000,
        'metal' : 2000,
        'pop' : 2000,
        'reggae' : 2000,
        'rock' : 2000
        }

    for t in rename_tracks:

        if t[0] == "r":
            tcsv = csv_tracks["%s_%04d" % (t[1], int(t[2]))]
            out = (t[3], tcsv[1], tcsv[2], unicode(count[t[3]]), tcsv[4], tcsv[5])
            count[t[3]]+=1
            output.append(out)

        csv_tracks.pop("%s_%04d" % (t[1], int(t[2])))

    print len(csv_tracks.keys())
    
    print len(output)
    output.extend(csv_tracks.values())
    random.shuffle(output)
    output = sorted(output, key=lambda x : x[0])
    final_output = []
    print len(output)
    
    count = dict()

    k = 0
    prev_genre = ""
    for i in output:
        if prev_genre != i[0]:
            k = 0
            prev_genre = i[0]

        if i[0] not in count:
            count[i[0]] = 0

        if count[i[0]] > max_tracks-1:
            continue

        count[i[0]]+=1

        final_output.append((i[0], i[1], i[2], unicode(k), i[4], i[5]))
        k+=1
    
    output_file = codecs.open(output_filename, mode='w', encoding='utf-8')
    output_file.write("genre;title;artist;genre_trackid;url;duration;\n")

    for i in final_output:
        output_file.write("%s;%s;%s;%s;%s;%s;\n" % (i[0], i[1], i[2], i[3], i[4], i[5]))
        print i

    print count





