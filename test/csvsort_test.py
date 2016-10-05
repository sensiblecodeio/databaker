from __future__ import absolute_import
from databaker.utf8csv import UnicodeWriter, UnicodeReader
import subprocess

sample = [["header"],
          ["L1","8","z","z","z"],
          ["L2","7","y","z","z"],
          ["L3","2","a","a","a"],
          ["L4","3","b","a","a"],
          ["L5","4","a","a","b"],
          ["L6","6","z","z"],
          ["L7","5","q","q","q","q"],
          ["footer"]]

with open("test/t_csvsort.csv", "w") as f:
    csvout = UnicodeWriter(f)
    for row in sample:
        csvout.writerow(row)

subprocess.call(["python", "databaker/sortcsv.py", "--header", "--footer", "4,3,2", "test/t_csvsort.csv"])

with open("test/t_csvsort.csv", "r") as f:
    csvin = list(UnicodeReader(f))
    body = csvin[1:-1]
    order = [x[1] for x in body]
    assert order==sorted(order), order
