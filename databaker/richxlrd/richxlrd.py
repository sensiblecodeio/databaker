class RichCell(object):
    def __init__(self, sheet, y, x):
        self.sheet = sheet
        self.y = y
        self.x = x

    @property
    def cell(self):
        return self.sheet.cell(self.y, self.x)

    @property
    def raw_fontlist(self):
        """the position of a font change, and the new font code.
           note that it doesn't include the first font!"""
        return self.sheet.rich_text_runlist_map.get((self.y, self.x), [])

    @property
    def first_font(self):
        """the first font number"""
        xf = self.cell.xf_index
        return self.sheet.book.xf_list[xf].font_index

    @property
    def fontlist(self):
        full_fontlist = list(self.raw_fontlist)
        full_fontlist.insert(0, (0, self.first_font))
        return list((pos, self.sheet.book.font_list[font]) for pos, font in full_fontlist)

def foo():
    print "foo"
