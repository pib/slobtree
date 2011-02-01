import json

class Index(object):
    def __init__(self, filename):
        self.f = open(filename, 'a')

    def insert(self, key, val):
        self.f.write('\n')
        self.f.write(json.dumps({"data": [[key, val]]}, separators=(',', ':')))
        self.f.flush()