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

    @property
    def fragments(self):
        fontlist = self.fontlist
        output = Fragments()
        for i, (start, font) in enumerate(fontlist):
            try:
                end = fontlist[i+1][0]
            except IndexError:
                end = None
            output.append(Fragment(self.cell.value[start:end], font))
            start = end
        return output

class Fragments(list):
    @classmethod
    def from_rich_text(self, richtext):
        return richtext.fragments

    def no_script(self):
        return Fragments(frag for frag in self if not frag.font.escapement)

    @property
    def value(self):
        return ''.join(x.text for x in self)

class Fragment(object):
    def __init__(self, text, font):
        self.text = text
        self.font = font

    def __repr__(self):
        return "<{!r}:{!r}>".format(self.text, self.font)
