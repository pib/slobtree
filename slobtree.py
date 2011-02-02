import errno
import os
import json


class Index(object):
    def __init__(self, filename):
        f = self.f = open(filename, 'ab+')

        offset = 0
        last_nl = -1
        while last_nl < 0 and f.tell() > 0:
            offset += 1024
            try:
                f.seek(-offset, os.SEEK_END)
            except IOError, e:
                if e.errno != errno.EINVAL:
                    raise
                f.seek(0)
            content = f.read(offset)
            last_nl = content.rfind('\n')
        if last_nl > 0:
            self.root = json.loads(content[last_nl:])
        else:
            self.root = None

    def insert(self, key, val):
        self.f.write('\n')
        self.f.write(json.dumps({"data": {key: val}}, separators=(',', ':')))
        self.f.flush()

    def search(self, key):
        return 'bar'
