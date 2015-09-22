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
        self.debug = False
        self.params = []

class datematch(unittest.TestCase):
    def test_datematch(self):
        self.assertEqual(bake.datematch("1999"), "Year")
        self.assertEqual(bake.datematch("2014 Q3"), "Quarter")
        self.assertEqual(bake.datematch("Jan-Apr 1982"), "Quarter")
        self.assertEqual(bake.datematch("Feb 2001"), "Month")
        self.assertEqual(bake.datematch("Not A Date"), "")
        self.assertEqual(bake.datematch(4.0), "")

class subdim(unittest.TestCase):
    def test_subdim(self):
        bake.Opt = Options(recipe='subdim_recipe.py', xls='glue.xls')
        recipe = imp.load_source("recipe", bake.Opt.recipe_file)
        for fn in bake.Opt.xls_files:
            bake.per_file(fn, recipe)
        with open("test/t_out.csv") as f:
            for row in UnicodeReader(f):
                if '- Q1 1997' in row:
                    return
        assert False, "No '- Q1 1997' in subdim"

class subdim(unittest.TestCase):
    def test_subdim(self):
        bake.Opt = Options(recipe='glue_recipe.py', xls='glue.xls')
        recipe = imp.load_source("recipe", bake.Opt.recipe_file)
        for fn in bake.Opt.xls_files:
            bake.per_file(fn, recipe)
        with open("test/t_out.csv") as f:
            for row in UnicodeReader(f):
                if row[0] == "8828.0":
                    assert "All Work  " in row, row
                    assert "2014.0" in row, row
                    return
        assert False, "No 8828 for 2014 All Work"

class no_tab_run(unittest.TestCase):
    def test_normal(self):
        bake.Opt = Options(recipe='bail.py', xls='t.xls')
        recipe = imp.load_source("recipe", bake.Opt.recipe_file)
        try:
            for fn in bake.Opt.xls_files:
                bake.per_file(fn, recipe)
        except SystemExit:
            pass
        else:
            raise Exception, "Should have been System Exit"

class super_sub_script(unittest.TestCase):
    def test_header(self):
        with open("test/t_out.csv", "w") as f:
            f.write('blat')
        bake.Opt = Options(recipe="supersub.py", xls="supersub.xls")
        recipe = imp.load_source("recipe", bake.Opt.recipe_file)
        for fn in bake.Opt.xls_files:
            bake.per_file(fn, recipe)
        with open("test/t_out.csv") as f:
            raw = list(UnicodeReader(f))
            assert "OB" in raw[1]
            assert "HEADER" in raw[1]


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
        self.assertEqual(set([u'', '4']), setdata[0])
        assert '(d)' in setdata[1]

        self.assertEqual(set(['Jan 2001', '2010', 'Jan-Mar 2005']), setdata[17])
        self.assertEqual(setdata[18], setdata[17])
        self.assertEqual(set(['Year', 'Quarter', 'Month']), setdata[20])

        self.assertEqual(set(["header_1"]), setdata[35])
        self.assertEqual(set(["ref"]), setdata[35+8])
        self.assertEqual(set(["table"]), setdata[35+8+8])

        self.assertEqual(setdata[38], set(["static_value"]))
        self.assertEqual(setdata[38+8], set(u'B2 B3 B4 C2 C3 C4 D2 D3 D4'.split(' ')))
        self.assertEqual(setdata[38+8+8], set(["Sheet1"]))

    def test_parse_ob(self):
        bake.Opt = Options(recipe='obs.py', xls='rich.xls')
        recipe = imp.load_source("recipe", bake.Opt.recipe_file)
        bake.Opt.preview_filename = "t_rich.xls"
        bake.Opt.csv_filename = "t_rich.csv"
        for fn in bake.Opt.xls_files:
            bake.per_file(fn, recipe)
