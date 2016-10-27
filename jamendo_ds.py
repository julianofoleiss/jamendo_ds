# -*- coding: utf-8 -*-

import json
import requests
import os
import codecs
from pprint import pprint
from multiprocessing import Pool

def load_clientid():
    with open('client_id.txt') as f:
        content = f.readlines()
    return content[0]

CLIENT_ID = load_clientid()
OUTPUT_FOLDER = "./jamendo_gtzan/"

if CLIENT_ID == "youridhere":
    print("Please set your jamendo client_id in client_id.txt!")
    exit(1)

#abaixo segue uma parametrização para encontrar por gênero...
#https://groups.google.com/forum/#!topic/jamendo-dev/3CmJzDiSBBY


def get_genre_filelist(genre, offset=0, limit=10, fmt='jsonpretty', cc=['ccnc'], metadata='musicinfo',
                       order='relevance', featured=1, groupby=''):
    # wrapper to call this API: https://developer.jamendo.com/v3.0/tracks
    #according to groups link above, if one should prioritize weekly popularity:
        # order=relevance+popularity_week_desc
        # boost=popularity_week

    """

    :param genre: genre to be searched
    :type genre: str
    :param offset: the position to start returning results from
    :type offset: int
    :param limit: maximum number of tracks returned. min(limit, 200)
    :type limit: int
    :param fmt: REST response format. one of: json, jsonpretty, xml
    :type fmt: str
    :param cc: list of creative commons licences to be filtered by. Jamendo takes care of precedence. May be ccsa, ccnc, ccnd
    :type cc: list[str]
    :param metadata: which metadata to include in response. A space-separated string of: musicinfo lyrics stats licenses
    :type metadata: str
    :param order: order results by this. check jamendo api docs.
    :type order: str
    :param featured: return only jamendo curated tracks
    :type featured: int
    :param groupby: group all results from an artist or album. It does not return an aggregated result: it truncates all tracks
        except for the first in the group. Valid values are *artist_id* and *album_id*.
    :type groupby: str
    """

    lic = ""
    for k in cc:
        lic += k + "=true&"

    request = "https://api.jamendo.com/v3.0/tracks/?client_id=%s&featured=%d&type=single albumtrack&order=%s&tags=%s&offset=%d&limit=%d&format=%s&include=%s&groupby=%s&%s" \
              % (CLIENT_ID, featured, order, genre, offset, limit, fmt, metadata, groupby, lic)
    response = requests.get(request)
    #print response.content

    return request, response


def get_genre_max_filelist(genre, max_tracks=1000, fmt='jsonpretty', cc=['ccsa'], metadata='musicinfo', order='relevance', featured=1, groupby=''):
    query_step = 200
    max_filelist = None
    for k in xrange(0, max_tracks, 200):
        print "getting %s tracks: %d-%d" % (genre, k, k+200-1)
        req, resp = get_genre_filelist(genre, offset=k, limit=200, fmt=fmt, cc=cc, metadata=metadata, order=order, featured=featured, groupby=groupby)

        j = json.loads(resp.content)

        r_count = j['headers']['results_count']

        print "%d tracks returned. " % r_count

        if j['headers']['status'] != "success":
            print "request failed! request string: %s.\nERROR:%s" % (req, resp['headers']['error_message'])
            return None

        if r_count == 0:
            break

        if max_filelist is None:
            max_filelist = j
        else:
            max_filelist['results'].extend(j['results'])

        if r_count < query_step:
            break

    max_filelist = max_filelist['results']
    print "%d tracks in filelist" % (len(max_filelist))

    final_list = []
    u = {}
    #get unique tracks
    for x in max_filelist:
        if not (x['id'] in u):
            u[x['id']] = x
    final_list = u.values()

    #make make a dict of tracks per artist
    artists = {}
    for x in final_list:
        if x['artist_id'] not in artists:
            artists[x['artist_id']] = []
        artists[x['artist_id']].append(x)


    # make make a dict of tracks per artist
    albums = {}
    for x in final_list:
        if x['album_id'] not in albums:
            albums[x['album_id']] = []
        albums[x['album_id']].append(x)

    # for i in artists:
    #     print i, len(artists[i])

    print "%d distinct tracks in filelist" % (len(final_list))
    print "%d distinct artists in filelist" % (len(artists))
    print "%d distinct albums in filelist" % (len(albums))
    #print req

    return final_list, artists, albums


def download_song(song_data):
    name = song_data[0]
    url = song_data[1]
    n = song_data[2]

    req = url
    mp3_data = requests.get(req)
    print('downloading song %d: %s...' % (n, name) )
    f = open( OUTPUT_FOLDER + name + '.mp3', 'w')
    f.write(mp3_data.content)
    f.close()


def slugify(string):
    remap = {
        ord("\t") : ord(" "),
        ord("\n") : None,
        ord("\f") : ord(" "),
        ord("\r") : None,
        ord("/") : ord(" ")
    }

    s = string.translate(remap)
    s = s.replace("&quot;", "")
    s = s.replace("&amp;", "")

    return s

def tally_classes(work):
    classes = {}
    for i in work:
        label = i[0].split("_")[0]
        if label not in classes:
            classes[label] = 0
        classes[label]+=1

    return classes

def from_csv(csv_filename="jamendo_list.csv", song_dir="./jamendo_downloaded/"):

    if song_dir[-1] != "/":
        song_dir += "/"
    
    OUTPUT_FOLDER = song_dir

    with codecs.open(csv_filename, "r", encoding='utf-8') as f:
        contents = f.readlines()
    
    work = []

    for i in xrange(1, len(contents)):
        track = contents[i].replace("\"", "").split(";")
        genre = track[0].strip()
        song_name = track[1].strip()
        artist_name = track[2].strip()
        songno = track[3].strip()
        url = track[4].strip()

        work.append((genre + "_" + songno , url, i) )
    
    pool = Pool(processes=4)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print("Downloading %d songs to %s..." % (len(work), OUTPUT_FOLDER))

    pool.map(download_song, work)    


def query_tags(genres, list_file="jamendo_list.csv"):

    file_list = codecs.open(list_file, "w", encoding='utf-8')
    file_list.write("genre;song;artist;songno;downloadurl;\n")

    if type(genres) != list:
        genres = [genres]
    
    work = []
    k = 0
    
    for genre in genres:
        lst, artists, albums = get_genre_max_filelist(genre, cc=[], max_tracks=1000, groupby='')

        artists = artists.values()

        for i in artists:
            k+=1
            song = i[0]

            song_name = slugify(song['name'])
            artist_name = slugify(song['artist_name'])

            #file_list.write("\"%s\";\"%s\";\"%s\";\"%s\"\n" % (genre, song_name, artist_name, song['audiodownload']))

            work.append((genre + "_" + song_name + " (" + artist_name + ")", song['audiodownload'], k) )


    print("%d tracks were retrieved" % (len(work)))

    print("summary of retrieved tracks:")
    pprint(tally_classes(work))

    #removing repeated tracks
    links = {}
    for i in work:
        if i[1] not in links:
            links[i[1]] = []
        links[i[1]].append(i)

    #for i in links:
    #    if len(links[i]) > 1:
    #        pprint(links[i])

    filtered_work = []
    for i in links:
        if len(links[i]) == 1:
            filtered_work.append(links[i][0])

    print("%d unique tracks were retrieved" % (len(filtered_work)))

    print("summary of retrieved (filtered) tracks:")
    pprint(tally_classes(filtered_work))

    filtered_work = sorted(filtered_work, key=lambda x: x[0].split("_")[0])

    prev_genre = "nenhum"
    songno = 0

    for song in filtered_work:
        genre = song[0].split("_")[0]
        artist_name = song[0].split("(")[1].replace(")", "")
        song_name = song[0].replace(genre + "_", "").replace("(" + artist_name + ")", "")

        if genre != prev_genre:
            prev_genre = genre
            songno = 0

        file_list.write("\"%s\";\"%s\";\"%s\";%04d;\"%s\"\n" % (genre, song_name, artist_name, songno, song[1]))
        songno+=1

if __name__ == "__main__":

    genre = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

    query_tags(genre)

