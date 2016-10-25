import jamendo_ds as jd
import sys

def print_usage():
    print("%s must be followed by either csv or newlist:" % (sys.argv[0]))
    print("\t csv csv_file songdir - downloads all tracks in csv_file in jamendo_ds format to songdir")
    print("\t newlist list_file songdir query_term1 query_term2 ... query_termn - queries the jamendo service for the n terms that follow newlist. This creates \
list_file (defaults to jamendo_list.csv) in jamendo_ds format and downloads all corresponding mp3 files to songdir (defaults to jamendo_downloaded).")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print_usage()
        exit(1)

    if sys.argv[1] == 'newlist':

        if len(sys.argv) < 5:
            print_usage()
            exit(1)

        listf = sys.argv[2]
        songd = sys.argv[3]
        query_terms = []
        for i in xrange(4, len(sys.argv)):
            query_terms.append(sys.argv[i])

        #["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

        jd.with_genres( query_terms , list_file=listf, song_dir=songd)

    elif sys.argv[1] == "csv":
        
        listf = sys.argv[2]
        songd = sys.argv[3]
        jd.from_csv(listf, songd)

    elif sys.argv[1] in ["--help", "-h", "-?"]:
        print_usage()
        exit(1)
    else:
        print("Invalid option!")
        print_usage()
        exit(1)

    

