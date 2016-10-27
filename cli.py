import jamendo_ds as jd
import sys

def print_usage():
    print("%s must be followed by either csv or newlist:" % (sys.argv[0]))
    print("\t csv csv_file songdir - downloads all tracks in csv_file in jamendo_ds format to songdir")
    print("\t query list_file query_term1 query_term2 ... query_termn - queries the jamendo service for the n terms that follow newlist. This creates \
list_file (defaults to jamendo_list.csv) in jamendo_ds format.")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print_usage()
        exit(1)

    if sys.argv[1] == 'newlist':

        if len(sys.argv) < 4:
            print_usage()
            exit(1)

        listf = sys.argv[2]
        query_terms = []
        for i in xrange(3, len(sys.argv)):
            query_terms.append(sys.argv[i])

        #["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

        jd.query_tags( query_terms , list_file=listf)

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

    

