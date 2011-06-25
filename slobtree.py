import errno
import os
import json


class Index(object):
    def __init__(self, filename, branching_factor=1024):
        self.branching_factor = branching_factor
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

    def _write_node(self, node):
        self.f.write('\n')
        position = self.f.tell()
        self.f.write(json.dumps(node, separators=(',', ':')))
        self.f.flush()
        return position

    def _find_node(self, _key):
        return self.root

    def _insert_node_data(self, node, key, val):
        data = node['data']
        for i in range(0, len(data)):
            if key < data[i][0]:
                data.insert(i, [key, val])
                return
        data.append([key, val])

    def insert(self, key, val):
        node = self._find_node(key) or {"data": []}
        self._insert_node_data(node, key, val)
        self._write_node(node)
        self.root = node

    def search(self, key):
        data = self.root.get('data', [])
        for k, val in data:
            if key == k:
                return val
        return None
