import errno
import os
import json


class Index(object):
    def __init__(self, filename):
        self.f = open(filename, 'ab+')
        self.root = None
        self._read_root()

    def _read_root(self):
        self.f.seek(0, os.SEEK_END)
        offset = 0
        last_nl = -1
        while last_nl < 0 and self.f.tell() > 0:
            offset += 1024
            try:
                self.f.seek(-offset, os.SEEK_END)
            except IOError, e:
                if e.errno != errno.EINVAL:
                    raise
                self.f.seek(0)
            content = self.f.read(offset)
            last_nl = content.rfind('\n')
        if last_nl > -1:
            self.root = json.loads(content[last_nl:])

    def insert(self, key, val):
        self.f.write('\n')
        self.f.write(json.dumps({"data": {key: val}}, separators=(',', ':')))
        self.f.flush()

    def search(self, key):
        return self.root.get('data', {}).get(key)
