import subprocess
import glob
import sys
import os


def get_song_duration(filename):

    command = ['soxi', filename]

    proc = subprocess.check_output(command)
    proc = proc.replace(" ", "")
    proc = proc.split("\n")

    duration = proc[5].split(":")

    duration = float(duration[1]) * 3600 + float(duration[2]) * 60 + float(duration[3].split("=")[0])

    print ("trimming %s (%.2fs) to 30s..." %  (filename, duration)  )

    return duration

def human_readable(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s

def trim_middle(infile, outfile, position, duration):

    ini = int(position - (duration / 2))
    end = int(position + (duration / 2))
    
    h, m, s = human_readable(ini)
    ini = "%02d:%02d:%02d" % (h, m, s)

    h, m, s = human_readable(end)
    end = "%02d:%02d:%02d" % (h, m, s)

    command = [ "sox", infile, outfile, "trim", str(ini), "=" + str(end) ]

    subprocess.call(command)

if __name__ == "__main__":

    mp3folder = sys.argv[1]
    clipped_folder = sys.argv[2]

    if clipped_folder[-1] != "/":
        clipped_folder +="/"

    if not os.path.exists(clipped_folder):
        os.makedirs(clipped_folder)

    songs = sorted([i for i in glob.glob( mp3folder + '/*.mp3')])

    for song in songs:
        duration = get_song_duration(song)
        filename = os.path.splitext(song)[0].split("/")[-1]
        trim_middle(song, clipped_folder + filename + "_trimmed.mp3", duration / 2, 30)
    
