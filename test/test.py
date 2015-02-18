import databaker.bake as bake
import unittest
import warnings
import imp
warnings.simplefilter("ignore")

class Options(object):
    def __init__(self, recipe, xls):
        self.xls_files = ['test/' + xls]
        self.recipe_file = 'test/' + recipe
        self.timing = False
        self.preview = False
        self.preview_filename = "test/t_out.xls"
        self.csv_filename = "test/t_out.csv"
        self.csv = False

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
