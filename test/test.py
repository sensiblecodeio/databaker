import databaker.bake as bake
import unittest
import warnings
import imp
from databaker.utf8csv import UnicodeReader

warnings.simplefilter("ignore")

class Options(object):
    def __init__(self, recipe, xls):
        self.xls_files = ['test/' + xls]
        self.recipe_file = 'test/' + recipe
        self.timing = True
        self.preview = True
        self.preview_filename = "t_out.xls"
        self.csv_filename = "t_out.csv"
        self.csv = True

class datematch(unittest.TestCase):
    def test_datematch(self):
        self.assertEqual(bake.datematch("1999"), "Year")
        self.assertEqual(bake.datematch("2014 Q3"), "Quarter")
        self.assertEqual(bake.datematch("Jan-Apr 1982"), "Quarter")
        self.assertEqual(bake.datematch("Feb 2001"), "Month")
        self.assertEqual(bake.datematch("Not A Date"), "")
        self.assertEqual(bake.datematch(4.0), "")

class normal_run(unittest.TestCase):
    def test_normal(self):
        bake.Opt = Options(recipe='t.py', xls='t.xls')
        recipe = imp.load_source("recipe", bake.Opt.recipe_file)
        for fn in bake.Opt.xls_files:
            bake.per_file(fn, recipe)
        with open("test/t_out.csv") as f:
            raw = list(UnicodeReader(f))
        self.assertEqual(raw[0][0], 'observation')
        self.assertEqual(raw[-1][0], '*'*9)
        self.assertEqual(raw[-1][1], '9')
        data = zip(*raw[1:-1])  # transpose
        setdata = [set(x) for x in data]
        print list(enumerate(setdata))
        self.assertEqual(set(['Jan 2001', '2010', 'Jan-Mar 2005']), setdata[17])
        self.assertEqual(setdata[18], setdata[17])
        self.assertEqual(set(['Year', 'Quarter', 'Month']), setdata[19])

        self.assertEqual(set(["header_1"]), setdata[35])
        self.assertEqual(set(["ref"]), setdata[35+8])
        self.assertEqual(set(["table"]), setdata[35+8+8])

        self.assertEqual(setdata[38], set(["static_value"]))
        self.assertEqual(setdata[38+8], set(x.upper() for x in data[1]))
        self.assertEqual(setdata[38+8+8], set(["Sheet1"]))








