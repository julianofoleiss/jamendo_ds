import subprocess
import glob
import sys
import os
from multiprocessing import Pool

def trim_middle(infile, outfile, position, duration):
    ini = int(position - (duration / 2))
    end = int(position + (duration / 2))
    
    h, m, s = human_readable(ini)
    ini = "%02d:%02d:%02d" % (h, m, s)

    h, m, s = human_readable(end)
    end = "%02d:%02d:%02d" % (h, m, s)

    command = [ "sox", infile, outfile, "trim", str(ini), "=" + str(end) ]

    subprocess.call(command)

def downsample(infile, outfile, mix, rate):

    command = "sox %s %s " % (infile, outfile)

    if mix_channels:
        command += "channels 1 "

    for i in range(6):
        command += "lowpass %d " % ( int(rate / 2))
    
    command += "rate %d " % (rate)

    subprocess.call(command, shell=True)

def downsample_thread(work):

    song = work[0]
    path = work[1]
    mix = work[2]
    rate = work[3]
    print("Downsampling %s to %dHz..." % (path, rate))

    downsample(song, path, mix, rate)

if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("Usage: %s mp3_folder out_folder rate input_extension" % sys.argv[0])
        exit(1)

    mp3folder = sys.argv[1]
    out_folder = sys.argv[2]
    rate = int(sys.argv[3])
    input_format = sys.argv[4]

    out_format = "wav" if "towav" in sys.argv else "mp3"
    mix_channels = True if "mixchannels" in sys.argv else False

    if out_folder[-1] != "/":
        out_folder +="/"

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    print mp3folder + '/*.%s' % input_format

    songs = sorted([i for i in glob.glob( mp3folder + '/*.%s' % input_format)])

    pool = Pool(4)

    work = []

    for song in songs:
        filename = os.path.splitext(song)[0].split("/")[-1]
        work.append((song, out_folder + filename + "_%dHz." % (rate) + out_format, mix_channels, rate))
    
    pool.map(downsample_thread, work)
    
    print("Done!")
