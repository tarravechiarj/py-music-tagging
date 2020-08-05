
import json
from mutagen.easyid3 import EasyID3

class AlbumTag(object):

    def __init__(self, tags=None):
        self.tags = []
        self.sorted = True
        self.data = { 'tags' : self.tags, 'sorted' : self.sorted }
        if tags:
            self.addTags(tags)

    def addTags(self, iterable):
        for i in iterable:
            self.addTag(i)
            
    def addTag(self, tag):
        self.tags.append(tag)
        self.sorted = False

    def sortTags(self):
        def sortKey(x):
            try:
                return abs(int(x))
            except:
                return str(x)

        def keyFilter(iterable, key, classinfo):
            return [x for x in iterable if isinstance(key(x), classinfo)]

        if not self.sorted:
            disc = lambda t: sortKey(t.get('discnumber' ''))
            track = lambda t: sortKey(t.get('tracknumber', ''))
        
            intDiscs = keyFilter(self.tags, disc, int)
            strDiscs = keyFilter(self.tags, disc, str)

            int_int = sorted(keyFilter(intDiscs, track, int), key=track)
            int_str = sorted(keyFilter(intDiscs, track, str), key=track)
            intDiscs = sorted(int_int + int_str, key=disc)

            str_int = sorted(keyFilter(strDiscs, track, int), key=track)
            str_str = sorted(keyFilter(strDiscs, track, str), key=track)
            strDiscs = sorted(str_int + str_str, key=disc)

            self.tags = intDiscs + strDiscs
            self.sorted = True

    def updateTags(self, newTagInfo, validate=False):
        for tag in self.tags:
            tag.update(newTagInfo)
        
        if 'discnumber' in newTagInfo or 'tracknumber' in newTagInfo:
            self.sorted = False

    def getTags(self, sort=True, validate=False):
        if sort:
            self.sortTags()
        
        if validate:
            self.removeInvalidTags()

        for tag in self.tags:
            yield tag

    def removeInvalidTags(self):
        valid = EasyID3.valid_keys.keys()

        for tag in self.tags:
            for k in tag:
                if k not in valid:
                    del tag[k]
                    print('WARNING: Invalid EasyID3 tag: {}'.format(k))

    def dump(self, file, sort=True):
        if sort:
            self.sortTags()

        json.dump(self.data, file)

    def load(self, file, sort=False):
        self.data = json.load(file)
        self.sorted = self.data['sorted']
        self.tags = self.data['tags']

        if sort:
            self.sortTags()



class SanitizedTags(AlbumTag):

    def sanitize(self, tag):
        keys = ('discnumber', 'tracknumber')
        keyFormats = (lambda x: str(x), lambda x: '{:02}'.format(x))

        for key, keyFormat in zip(keys, keyFormats):
            if key not in tag:
                continue
            
            keyStr = str(tag[key])

            if keyStr.isdigit():
                keynum = int(keyStr)
            elif len(keyStr) == 1 and keyStr.isalpha():
                keynum = 1 + ord(keyStr.upper()) - ord('A')
            else:
                keynum = 0
            
            tag[key] = keyFormat(keynum)

    def flatten(self):
        if not self.tags:
            return
        
        self.sortTags()

        mindisc = tags[0].get('discnumber')
        currentdisc = mindisc
        addend = 0
        for i, tag in enumerate(tags):
            if currentdisc != tag.get('discnumber'):
                currentdisc = tag.get('discnumber')
                addend = tags[i-1].get('tracknumber', 0)
            if currentdisc != mindisc:
                tag['tracknumber'] += addend
                tag['discnumber'] = mindisc

    def addTag(self, tag):
        self.sanitize(tag)
        self.tags.append(tag)
        self.sorted = False

    def sortTags(self):
        if not self.sorted:
            self.tags.sort(key=lambda t: int(t.get('tracknumber', 0)))
            self.tags.sort(key=lambda t: int(t.get('discnumber', 0)))
            self.sorted = True    

    def removeSingleDiscInfo(self):
        self.sortTags()

        if self.tags[0].get('discnumber') == self.tags[-1].get('discnumber'):
            for k in self.tags:
                if 'discnumber' in k:
                    del k['discnumber']

    def getTags(self, sort=True, validate=False, ):
        if sort:
            self.sortTags()
        
        if validate:
            self.removeInvalidTags()

        for tag in self.tags:
            yield tag

    def load(self, file, sort=False):
        self.data = json.load(file)
        self.sorted = self.data['sorted']
        self.tags = self.data['tags']

        for tag in tags:
            self.sanitize(tag)

        if sort:
            self.sortTags()
