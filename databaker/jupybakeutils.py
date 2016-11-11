# HTML preview of the dimensions and table (will be moved to a function in databakersolo)

from IPython.display import display
from IPython.core.display import HTML
import databaker.constants
OBS = databaker.constants.OBS

# copied out again
def create_colourlist():
    # Function to dynamically assign colours to dimensions for preview
    "https://github.com/python-excel/xlwt/blob/master/xlwt/Style.py#L309"
    colours = ["lavender", "violet", "gray25", "sea_green",
              "pale_blue", "blue", "gray25", "rose", "tan", "light_yellow", "light_green", "light_turquoise",
              "light_blue", "sky_blue", "plum", "gold", "lime", "coral", "periwinkle", "ice_blue", "aqua"]
    numbers = []
    for i in range(len(databaker.constants.template.dimension_names)-1, \
                   -(len(colours) - len(databaker.constants.template.dimension_names)), -1):
        numbers.append(-i)
    colourlist = dict(list(zip(numbers, colours)))
    return colourlist
colourlist = create_colourlist()
colchange = {"rose":"misty_rose", "ice_blue":"cornflower_blue", "periwinkle":"burly_wood", "pale_blue":"deep_sky_blue", "gray25":"light_gray", "light_turquoise":"pale_turquoise"}


def tsubsets(headers, segment):
    tsubs = [ ]
    if segment:
        tsubs.append((OBS, "OBS", segment))
    for i, header in headers.items():
        if header.direction is not None:   # filter out TempValue headers
            label = header.Dlabel
            if isinstance(label, int) and label < 0:
                label = databaker.constants.template.dimension_names[len(databaker.constants.template.dimension_names)-1+label]
            tsubs.append((i, label, header.bag))
    return tsubs

def dsubsets(dimensions, segment):
    tsubs = [ ]
    if segment:
        tsubs.append((OBS, "OBS", segment))
    for i, (header_bag, label, strict, direction) in enumerate(dimensions):
        if direction is not None:   # filter out TempValue headers
            if isinstance(label, int) and label < 0:
                label = databaker.constants.template.dimension_names[len(databaker.constants.template.dimension_names)-1+label]
            tsubs.append((i, label, header_bag))
    return tsubs


def tabletohtml(tab, tsubs):
    key = [ ]
    key.append('Table: ')
    key.append('<b>')
    key.append(tab.name); 
    key.append('</b> ')
    key.append('<table class="ex">\n')
    key.append('<tr>')
    ixyheaderlookup = { }
    for i, label, bag in tsubs:
        for h in bag:
            ixyheaderlookup[(h.x, h.y)] = i
        key.append('<td class="exc%d">' % i)
        key.append(label)
        key.append('</td>')
    key.append('</tr>')
    key.append('</table>\n')
    
    sty = [ ]
    sty.append("<style>\n")
    sty.append("table.ex td, table.ex tr { border: none }\n")
    sty.append("td.exbold { font-weight: bold }\n")
    sty.append("td.exnumber { color: green }\n")
    sty.append("td.exdate { color: purple }\n")
    sty.append("table { border-collapse: collapse }\n")
    for i, col in colourlist.items():
        sty.append("td.exc%d { background-color: %s }\n" % (i, "".join(lv.capitalize() for lv in colchange.get(col, col).split("_"))))
    sty.append("td.exc%d:hover { border: thin blue solid }\n" % OBS)
    sty.append("</style>\n\n")

    htm = [ ]
    htm.append('<table class="ex">\n')
    for row in tab.rows():
        htm.append("<tr>")
        assert len(row) == tab._max_x + 1
        rrow = sorted(row, key=lambda X: X.x)
        for c in rrow:
            cs = [ ]
            ih = ixyheaderlookup.get((c.x, c.y))
            if ih is not None:             cs.append("exc%d" % ih)
            if c.properties.get_bold():    cs.append("exbold")
            if c.is_date():                cs.append("exdate")
            if c.is_number():              cs.append("exnumber")
            htm.append('<td class="%s" title="(%d,%d)">' % (" ".join(cs), c.x, c.y))
            htm.append(str(c.value))
            htm.append("</td>")
        htm.append("</tr>\n")
    htm.append("</table>\n")

    jsty = "".join(sty)
    jkey = "".join(key)
    jhtm = "".join(htm)
    return "%s\n%s\n%s\n" % (jsty, jkey, jhtm)

inlinehtmidNUM = 1000
def inlinehtmldisplay(htm, hide=False):
    global inlinehtmidNUM
    inlinehtmidNUM += 1
    display(HTML('injblock%d: <div id="injblock%d" style="%s">%s</div>' % (inlinehtmidNUM, inlinehtmidNUM, "display:none" if hide else "display:inline", htm)))

def sidewindowhtmldisplay():
    sjs = '''
<script type="text/Javascript">
var injblock = document.getElementById("injblock%d"); 
console.log(injblock.innerHTML); 
var sidewin = window.open("", "abc123", "toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=780,height=200,top=200,left=200"); 
if (sidewin) 
    sidewin.document.body.innerHTML = injblock.innerHTML;
else
    alert("sidewindow didn't work"); 
</script>
'''
    display(HTML(sjs % inlinehtmidNUM))
    
    
