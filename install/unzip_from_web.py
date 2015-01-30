import sys
import requests
import zipfile
import StringIO
import re
import os

try:
    os.removedirs('databaker')
except Exception, e:
    print e
baseurl = 'https://github.com/scraperwiki/databaker/archive/{}.zip'
_, branch = sys.argv
print baseurl.format(branch)
r = requests.get(baseurl.format(branch))
z = zipfile.ZipFile(StringIO.StringIO(r.content))
z.extractall('.')
try:
    os.rename('databaker-{}'.format(branch), 'databaker')
except Exception, e:
    print e
