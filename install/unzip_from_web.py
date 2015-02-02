import sys
import requests
import zipfile
import StringIO
import os

baseurl = 'https://github.com/scraperwiki/databaker/archive/{}.zip'
_, branch = sys.argv
print baseurl.format(branch)
r = requests.get(baseurl.format(branch))
z = zipfile.ZipFile(StringIO.StringIO(r.content))
z.extractall('.')
os.rename('databaker-{}'.format(branch), 'databaker')
