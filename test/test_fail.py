from __future__ import absolute_import, division
import databaker.bake as bake
import databaker.constants as constants
import unittest
import imp
import warnings

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
        self.debug = False
        self.params = ["1999","2000"]

class paramfail(unittest.TestCase):
    def test_failparam(self):
        Opt = Options(recipe='paramfail.py', xls='t.xls')
        constants.constant_params = Opt.params
        recipe = imp.load_source("recipe", Opt.recipe_file)
        try:
            for fn in Opt.xls_files:
                bake.per_file(fn, recipe, Opt)
        except Exception as e:
            msg = repr(e)
            assert "NotEnoughParams" in msg
            assert 'PARAM(2)' in msg
            assert "['1999', '2000']" in msg
