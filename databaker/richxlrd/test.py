import unittest
import xlrd
from nose.tools import assert_equal
import richxlrd

class Test_Foo(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.wb = xlrd.open_workbook("rich.xls", formatting_info=True)
        self.sheet = self.wb.sheets()[0]
        self.cells = {}

        y=0
        while True:
            x=0
            while True:
                try:
                    cell = self.sheet.cell(y,x)
                except IndexError:
                    break
                if cell.value:
                    self.cells[(y, x)] = cell
                x=x+1
            print
            y=y+1
            if y>10:
                break

        self.sample = richxlrd.RichCell(self.sheet, 3, 2)

    def test_load(self):
        assert_equal(self.cells[(3, 2)].value, u'12015')

    def test_richcell_raw_fontlist(self):
        assert_equal(self.sample.fontlist, [(1,0)])
