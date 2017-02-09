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

def downsample(infile, outfile, mix):

    command = "sox %s %s " % (infile, outfile)

    if mix_channels:
        command += "channels 1 "

    for i in range(6):
        command += "lowpass 11025 "
    
    command += "rate 22050 "

    subprocess.call(command, shell=True)

def downsample_thread(work):

    song = work[0]
    path = work[1]
    mix = work[2]

    print("Downsampling %s to 22050KHz..." % path)

    downsample(song, path, mix)

if __name__ == "__main__":

    mp3folder = sys.argv[1]
    out_folder = sys.argv[2]

    out_format = "wav" if "towav" in sys.argv else "mp3"
    mix_channels = True if "mixchannels" in sys.argv else False

    if out_folder[-1] != "/":
        out_folder +="/"

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    songs = sorted([i for i in glob.glob( mp3folder + '/*.mp3')])

    pool = Pool(4)

    work = []

    for song in songs:
        filename = os.path.splitext(song)[0].split("/")[-1]
        work.append((song, out_folder + filename + "_22KHz." + out_format, mix_channels))
    
    pool.map(downsample_thread, work)
    
    print("Done!")
