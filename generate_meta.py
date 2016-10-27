import codecs
import sys

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("this program generates a genre meta file from a jamendo_ds csv")
        print("usage: %s jamendo_ds_csv metafile [prefix]")
        exit(1)

    csv_filename = sys.argv[1]
    meta_filename = sys.argv[2]

    prefix = sys.argv[3] if len(sys.argv) > 3 else ""

    with codecs.open(csv_filename, "r", encoding='utf-8') as f:
        contents = f.readlines()

    metafile = open(meta_filename, "w")

    for i in xrange(1, len(contents)):
        track = contents[i].replace("\"", "").split(";")
        genre = track[0].strip()
        song_name = track[1].strip()
        artist_name = track[2].strip()
        songno = track[3].strip()
        url = track[4].strip()

        metafile.write("%s%s_%s.mp3\t%s\n" % (prefix, genre, songno, genre))

    metafile.close()

    