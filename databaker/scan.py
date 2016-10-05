from __future__ import absolute_import, division
dims = [14, 17, 38, 46, 54, 62, 70]

from utf8csv import UnicodeReader

seen = set()
with open('out.csv', 'r') as f:
    for i, item in enumerate(UnicodeReader(f)):
        thisrow = []
        for dim in dims:
            try:
                thisrow.append(item[dim])
            except IndexError:
                break
        seen.add('!'.join(thisrow))
        assert len(seen) == i + 1, (thisrow)
