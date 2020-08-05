#!/usr/bin/env python

import argparse
import re
import sys
import json
from albumTag import SanitizedTags

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="a file containing title tag information")
    parser.add_argument("output", help="file to write output json file to")
    parser.add_argument("-j", "--json", help="json file containing album tag information")
    parser.add_argument("-f", "--flatten", action="store_true",
                        help="Treat album as being single-disc")
    parser.add_argument("-v", "--va", action="store_true",
                        help="Album is various-artist compilation")
    parser.add_argument("-k", "--keepDiscInfo", action="store_true",
                        help="Don't remove discnumber from single-disc album")
    return parser.parse_args()

"""
Parse lines consisting of a track number followed by a track title,
possibly preceded by a disc number and possibly followed by a 
duration (e.g. 6:00).
"""
def parseLine(line, va=False):
    trackpos1 = '^(?P<discnumber>\d+)\.(?P<tracknumber>\d+)\s+'
    trackpos2 = '^(?P<discnumber>[A-Z]?)(?P<tracknumber>\d*)\s+'
    artist = '(?P<artist>\S.*?\S)'
    title = '(?P<title>\S.*?\S)' 
    time = '(?:\s+\d+:\d+)?$'

    middle = artist + ' - ' + title if va else title

    p1 = trackpos1 + middle + time
    p2 = trackpos2 + middle + time

    for p in (p1, p2):
        m = re.match(p, line)
        if m is not None:
            ret = m.groupdict()
            for key in ('discnumber', 'tracknumber'):
                if not ret.get(key):
                    ret[key] = '1'
            return ret

    return None

def main():
    args = parseArgs()

    albumTag = SanitizedTags()

    with open(args.input) as f:
        for line in f:
            line = line.strip()
            trackTag = parseLine(line, args.va)
            if trackTag:
                albumTag.addTag(trackTag)

    if args.json:
        with open(args.json, 'r') as f:
            albumTag.updateTags(json.load(f))

    if args.flatten:
        albumTag.flatten()

    if not args.keepDiscInfo:
        albumTag.removeSingleDiscInfo()

    with open(args.output, 'w') as f:
        albumTag.dump(f)

if __name__ == '__main__':
    main()