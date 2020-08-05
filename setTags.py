#!/usr/bin/env python

import sys
import os
import argparse
import json
from albumTag import AlbumTag
from mutagen.easyid3 import EasyID3

def parseCmdLine():
    parser = argparse.ArgumentParser()
    parser.add_argument("json", help="json file containing tag information")
    parser.add_argument("dir", help="directory containing mp3 files")
    parser.add_argument("-r", "--recurse", help="write to files in subdirectories",
                        action="store_true")
    return parser.parse_args()

def formatTrackNo(num):
    try:
        return '{:02}'.format(int(num))
    except:
        return str(num)

def writeTag(filename, tag):
    id3 = EasyID3(filename)
    if 'tracknumber' in tag:
        tag['tracknumber'] = formatTrackNo(tag['tracknumber'])
    for k, v in tag.items():
        id3[k] = v
    id3.save()

def getFiles(dirname, recurse):
    files = []
    path = os.fsencode(dirname)
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir() and recurse:
                files.extend(getFiles(entry.path, recurse))
            elif entry.is_file():
                fname = os.fsdecode(entry.path)
                if fname.endswith('.mp3') or fname.endswith('.m4a'):
                    files.append(fname)
    return files

def main():
    args = parseCmdLine()

    try:
        albumtag = AlbumTag()
        with open(args.json) as f:
            albumtag.load(f)
        tags = albumtag.getTags(validate=True)
        files = getFiles(args.dir, args.recurse)
        files.sort()

        for file in files:
            writeTag(file, next(tags))

    except Exception:
        print("An exception occurred: " + str(sys.exc_info()))


if __name__ == '__main__':
    main()