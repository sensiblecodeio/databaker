class RichCell(object):
    def __init__(self, sheet, y, x):
        self.sheet = sheet
        self.y = y
        self.x = x

    @property
    def cell(self):
        return self.sheet.cell(self.y, self.x)

    @property
    def fontlist(self):
        return self.sheet.rich_text_runlist_map.get((self.y, self.x))

    def rich(self):
        print
        return runlist
        pass

def foo():
    print "foo"
