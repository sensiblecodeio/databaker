import unittest
import xlrd

class Test_Foo(unittest.TestCase):
    def test_fail(self):
        wb = xlrd.open_workbook("rich.xls", formatting_info=True)
        sheet = wb.sheets()[0]
        y=0
        while True:
            x=0
            while True:
                try:
                    print repr(sheet.cell(y,x).value),
                except IndexError:
                    break
                x=x+1
            print
            y=y+1
            if y>10:
                break

        assert False


