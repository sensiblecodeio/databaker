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


ndividNUM = 1000
dividNUM = "kkkk"
def incrementdividNUM():
    global ndividNUM, dividNUM
    ndividNUM += 1
    dividNUM = "injblock%d" % ndividNUM

def tabletohtml(tab, tsubs):
    key = [ ]
    key.append('Table: ')
    key.append('<b>')
    key.append(tab.name); 
    key.append('</b> ')
    key.append('<table class="exkey">\n')
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
    sty.append("table.ex td:hover { border: thin blue solid }\n")
    sty.append("table.ex td.exc%d:hover { border: thin red solid }\n" % OBS)
    sty.append("table.ex td.selected { background-color: red }\n")
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
            htm.append('<td class="%s" title="%d %d">' % (" ".join(cs), c.x, c.y))
            htm.append(str(c.value))
            htm.append("</td>")
        htm.append("</tr>\n")
    htm.append("</table>\n")

    jsty = "".join(sty)
    jkey = "".join(key)
    jhtm = "".join(htm)
    return "%s\n%s\n%s\n" % (jsty, jkey, jhtm)

jscode = """
<script>
var jslookup = %s; 
var jdividNUM = "%s"; 
var Dclickedcell = null; 
function clickedcell() 
{ 
    Dclickedcell = this; 
    console.log("jjjj", this); 
    var rgc = new RegExp('(^|\\b)' + "selected".split(' ').join('|') + '(\\b|$)', 'gi'); 
    Array.prototype.forEach.call(document.querySelectorAll("div#"+jdividNUM+" table.ex td.selected"), function(el, i) { 
        if (el.classList)  el.classList.remove("selected");
        else  el.className = el.className.replace(rgc, ' ');
    }); 
    if (this.classList)  this.classList.add("selected");
    else this.className += ' ' + "selected";

    var dimpairs = jslookup[this.title]; 
    if (dimpairs !== undefined) {
        for (var i = 1; i < dimpairs.length; i += 2) {
            var row = document.querySelectorAll("div#"+jdividNUM+" table.ex tr")[dimpairs[i]]; 
            var el = row.querySelectorAll("td")[dimpairs[i-1]]; 
            if (el.classList)  el.classList.add("selected");
            else el.className += ' ' + "selected";
        }
    }
}
Array.prototype.forEach.call(document.querySelectorAll("div#"+jdividNUM+" table.ex td"), function(item, i) { item.onclick=clickedcell; }); 
</script>
"""

def inlinehtmldisplay(htm, hide=False):
    display(HTML('%s: <div id="%s" style="%s">%s</div>' % (dividNUM, dividNUM, "display:none" if hide else "display:inline", htm)))

def inlinehtmljsactive(conversionsegment, batchcelllookup):
    # generate the lookup table from titles to references
    tab, dimensions, segment = conversionsegment
    obslist = list(segment.unordered_cells)  # list(segment) otherwise gives bags of one element
    dimvalues = [ batchcelllookup(tab, obslist, dimension)  for dimension in dimensions ]
    jslookup = '{%s}' % ",".join('"%d %d":[%s]' % (k.x, k.y, ",".join("%d,%d" % (d.x, d.y)  for d in tup))  \
                           for k, tup in zip(obslist, zip(*dimvalues)))
    display(HTML(jscode % (jslookup, dividNUM)))
    
# could do this as a save and reload
def sidewindowhtmldisplay():
    sjs = '''
<script type="text/Javascript">
var injblock = document.getElementById("%s"); 
console.log(injblock.innerHTML); 
var sidewin = window.open("", "abc123", "toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=780,height=200,top=200,left=200"); 
if (sidewin) 
    sidewin.document.body.innerHTML = injblock.innerHTML;
else
    alert("sidewindow didn't work"); 
</script>
'''
    display(HTML(sjs % dividNUM))
    
    
