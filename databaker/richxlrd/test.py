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
        self.normal = richxlrd.RichCell(self.sheet, 4, 4)
        self.alphabet = richxlrd.RichCell(self.sheet, 6, 4)

    def test_load(self):
        assert_equal(self.cells[(3, 2)].value, u'12015')

    def test_richcell_raw_fontlist(self):
        assert_equal(self.sample.raw_fontlist, [(1,0)])
        assert_equal(self.normal.raw_fontlist, [])

    def test_richcell_font_0(self):
        assert_equal(self.sample.first_font, 8)
        assert_equal(self.normal.first_font, 0)

    def test_richcell_fontlist(self):
        assert_equal(len(self.sample.fontlist), 2)
        assert_equal(len(self.normal.fontlist), 1)
        assert_equal(len(self.alphabet.fontlist), len(self.alphabet.cell.value))
        assert_equal(self.normal.fontlist[0][1], self.sample.fontlist[1][1])

    def test_fragments(self):
        frag = self.alphabet.fragments
        assert_equal(len(frag), len(self.alphabet.cell.value))
        assert frag[0].font == frag[2].font == frag[4].font
        assert frag[1].font == frag[3].font == frag[5].font
        assert frag[0].font != frag[1].font

    def test_classy_fragments(self):
        assert isinstance(self.sample.fragments, richxlrd.Fragments)
        assert isinstance(self.sample.fragments[0], richxlrd.Fragment)
