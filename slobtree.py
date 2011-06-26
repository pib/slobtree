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
        self.f.seek(0, os.SEEK_END)
        self.f.write('\n')
        position = self.f.tell()
        self.f.write(json.dumps(node, separators=(',', ':')))
        self.f.flush()
        return position

    def _read_node(self, offset):
        self.f.seek(offset)
        line = self.f.readline()
        return json.loads(line)

    def _is_key_node(self, node):
        if node and 'keys' in node:
            return True
        return False

    def _find_node(self, find_key):
        if not self.root:
            return None
        node = self.root
        path = [self.root]
        while self._is_key_node(node):
            last = None
            for key, offset in node['keys']:
                last = offset
                if key >= find_key:
                    break
            node = self._read_node(last)
            path.append(node)

        return path

    def _insert_node_data(self, node, key, val):
        data = node['data']
        for i in range(0, len(data)):
            if key < data[i][0]:
                data.insert(i, [key, val])
                return
        data.append([key, val])

    def insert(self, key, val):
        node_path = self._find_node(key) or [self.root, {"data": []}]
        node = node_path[-1]
        self._insert_node_data(node, key, val)
        if len(node['data']) > self.branching_factor:
            self._split_node(node)
        self._write_node(node)
        self.root = node

    def search(self, key):
        node_path = self._find_node(key) or [self.root, {"data": []}]
        data = node_path[-1].get('data', [])
        for k, val in data:
            if key == k:
                return val
        return None
