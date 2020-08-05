# py-music-tagging
Automate writing ID3 tags using Mutagen

### Use
If <album.json> is a json file containing ID3 tag information for the album as a whole and <album.txt> is a text file containing a track number and corresponding track title on each line, then
```
python parseTags.py -j <album.json> <album.txt> <out.json>
python setTags.py <out.json> <album directory>
```
will write the specified ID3 tags to the .mp3 or .m4a files in the specified album directory (The output of parseArgs is the first directional argument to setTags).

Use the following to see more options:
```
python parseTags.py -h
python setTags.py -h 
```
