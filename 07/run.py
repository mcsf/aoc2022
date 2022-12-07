#!/usr/bin/env python3

import sys


class File:
    def __init__(self, name, size):
        self.name = name
        self._size = size

    def size(self):
        return self._size


class Dir(File):
    def __init__(self, name, parent):
        self.files = {}
        self.name = name
        self.parent = parent
        self._size = None

    def size(self):
        if not self._size:
            self._size = sum(f.size() for f in self.files.values())
        return self._size


root = Dir('/', None)
curr = root
for line in sys.stdin:
    prefix, cmd, *arg = line.split()
    if prefix == '$':
        if cmd == 'cd':
            if arg[0] == '/':
                curr = root
            elif arg[0] == '..':
                curr = curr.parent
            else:
                curr = curr.files[arg[0]]
    else:
        data, name = line.split()
        if data == 'dir':
            curr.files[name] = Dir(name=name, parent=curr)
        else:
            curr.files[name] = File(name=name, size=int(data))


def dirs(dir):
    yield dir
    for d in dir.files.values():
        if isinstance(d, Dir):
            yield from dirs(d)


need = 30000000 - (70000000 - root.size())
print(sum(d.size() for d in dirs(root) if d.size() <= 100000))
print(min(d.size() for d in dirs(root) if d.size() >= need))

# In class File:
# def ls(self):
#     return f'- {self.name} (file, size={self.size()})'
#
# In class Dir:
# def __repr__(self):
#     return f'Dir(name={self.name})'
# def ls(self):
#     contents = '\n'.join(f.ls() for f in self.files.values())
#     contents = re.sub(r'^', '  ', contents, flags=re.M)
#     return f'- {self.name} (dir, size={self.size()})\n{contents}'
