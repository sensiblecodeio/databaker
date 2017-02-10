# encoding: utf-8

import io, os, collections, re, warnings

from IPython.display import display, FileLink
from IPython.core.display import HTML
import databaker.constants

OBS = databaker.constants.OBS   # used to evaluate to -9, does to "OBS" now

from databaker.jupybakeutils import HDim, ConversionSegment, svalue

# copied out again
def create_colourlist():
    # Function to dynamically assign colours to dimensions for preview
    colchange = {"rose":"misty_rose", "ice_blue":"cornflower_blue", "periwinkle":"burly_wood", "pale_blue":"deep_sky_blue", "gray25":"light_gray", "light_turquoise":"pale_turquoise"}
    "https://github.com/python-excel/xlwt/blob/master/xlwt/Style.py#L309"
    ocolours = ["aqua", "light_green", "rose", "gray25", "periwinkle", "coral", "gold", "lime", 
              "light_blue", "plum", "ice_blue", "light_yellow", 
              "lavender", "violet", "sea_green", 
              "pale_blue", "blue", "gray25", "light_turquoise", "tan", "sky_blue", 
]
              
    colours = [ "".join(lv.capitalize()  for lv in colchange.get(col, col).split("_"))  for col in ocolours ]
    numbers = list(range(len(colours)))
    colourlist = dict(list(zip(numbers, colours)))
    return colourlist
colourlist = create_colourlist()


ndividNUM = 1000
dividNUM = "kkkk"
def incrementdividNUM():
    global ndividNUM, dividNUM
    ndividNUM += 1
    dividNUM = "injblock%d" % ndividNUM

def tabletohtml(tab, tsubs, consolidatedcellvalueoverride, blocalstylesheet):
    key = [ ]
    key.append('Table: <b>%s</b> ' % tab.name)
    key.append('<table class="exkey">\n')
    key.append('<tr>')
    ixyheaderlookup = { }
    for i, label, bag in tsubs:
        for h in bag:
            ixyheaderlookup[(h.x, h.y)] = i
        if blocalstylesheet:
            key.append('<td class="xc%s">%s</td>' % (i, label))
        else:
            key.append('<td class="xc%s" style="background-color:%s">%s</td>' % (i, colourlist.get(i,"white"), label))
    key.append('</tr>')
    key.append('</table>\n')
    
    
    sty = [ ]
    sty.append("<style>\n")
    sty.append("table.ex, table.exkey { border: thin black solid }\n")
    sty.append("table.ex td, table.ex tr { border: none }\n")
    if blocalstylesheet:
        sty.append("td.xb { font-weight: bold }\n")
        sty.append("td.xn { color: green }\n")
        sty.append("td.xd { color: purple }\n")
        sty.append("span.xo { text-decoration: line-through; }\n")
        sty.append("span.xn { }\n")
        sty.append("table { border-collapse: collapse }\n")
        sty.extend("td.xc%d { background-color: %s }\n" % (i, col)  for (i, col) in colourlist.items())
    sty.append("table.ex td:hover { border: thin blue solid }\n")
    sty.append("table.ex td.exc%s:hover { border: thin red solid }\n" % OBS)
    if blocalstylesheet:
        sty.append("table.ex td.selected { background-color: red; border: thin blue dotted }\n")
    else:
        sty.append("table.ex td.selected { border: thick red solid }\n")
    sty.append("</style>\n\n")

    htm = [ ]
    htm.append('<table class="ex">\n')
    for row in tab.rows():
        htm.append("<tr>")
        assert len(row) == tab._max_x + 1
        rrow = sorted(row, key=lambda X: X.x)
        for c in rrow:
            ih = ixyheaderlookup.get((c.x, c.y))
            if blocalstylesheet:
                cs = [ ]
                if ih is not None:             cs.append("xc%s" % ih)
                if c.properties.get_bold():    cs.append("xb")
                if c.is_number():              cs.append("xn")
                htm.append('<td class="%s" title="%d %d">' % (" ".join(cs), c.x, c.y))
            else:
                ls = [ ]
                if ih is not None:             ls.append("background-color:%s" % colourlist.get(ih,"white"))
                if c.properties.get_bold():    ls.append("font-weight:bold")
                lss = ' style="%s"' % ";".join(ls)  if ls  else ''
                htm.append('<td%s title="%d %d">' % (lss, c.x, c.y))
                
            if (c.x, c.y) in consolidatedcellvalueoverride:
                prevcellval = svalue(c) or "*blank*" # want to see empty cells that have been overwritten
                overridecellval = consolidatedcellvalueoverride[(c.x, c.y)]
                if blocalstylesheet:
                    htm.append('<span class="xo">%s</span><span class="xn">%s</span>' % (prevcellval, overridecellval))
                else:
                    htm.append('<strike>%s</strike>%s' % (prevcellval, overridecellval))
            else:
                htm.append(svalue(c))
                
            if (c.x, c.y) in consolidatedcellvalueoverride:
                consolidatedcellvalueoverride
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

# generate the lookup table from titles to references
def calcjslookup(conversionsegment):
    obslist = list(conversionsegment.segment.unordered_cells)  # list(segment) otherwise gives bags of one element

    # this is where we could check/override the lookup values in some way
    dimvalues = [ [ hdim.cellvalobs(ob)[0]  for hdim in conversionsegment.dimensions  if hdim.hbagset is not None ]  for ob in obslist ]
    jslookup = '{%s}' % ",".join('"%d %d":[%s]' % (k.x, k.y, ",".join("%d,%d" % (d.x, d.y)  for d in tup  if d))  \
                           for k, tup in zip(obslist, dimvalues))
    return jslookup
    
    
# could do this as a html-frame and reload
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
    
    
def savepreviewhtml(conversionsegment, fname=None):
    
    # wrap a singleton or list of bags, tables and HDims to a ConversionSegment
    if not isinstance(conversionsegment, ConversionSegment): 
        param1 = conversionsegment
        if not isinstance(param1, (tuple, list)):
            param1 = [param1]
            
        tab = None
        dimensions = [ ]
        for i, p in enumerate(param1):
            if "Table" in str(type(p)):
                ltab = p
                lhdim = None
            elif isinstance(p, HDim):
                ltab = p.hbagset.table
                lhdim = p
            else:
                ltab = p.table
                lhdim = HDim(p, "item %d"%i, databaker.constants.DIRECTLY, databaker.constants.ABOVE)   # (fake lookup)
            
            if not tab:
                tab = ltab
            else:
                assert ltab is tab, "must all be same table"

            if lhdim:
                dimensions.append(lhdim)
                
        conversionsegment = ConversionSegment(tab, dimensions, [])
    
    # now we have a ConversionSegment
    incrementdividNUM()
    if fname is None:
        fout = io.StringIO()
        blocalstylesheet = not (len(conversionsegment.tab) < 1500)
    else:
        fout = io.open(fname, "w", encoding='utf-8')
        fout.write("<html>\n<head><title>%s</title><meta charset=\"UTF-8\"></head>\n<body>\n" % conversionsegment.tab.name)
        blocalstylesheet = True
        
    htmtable = tabletohtml(conversionsegment.tab, conversionsegment.dsubsets(), conversionsegment.consolidatedcellvalueoverride(), blocalstylesheet)
    fout.write('<div id="%s">#%s\n' % (dividNUM, dividNUM))
    fout.write(htmtable)
    fout.write('</div>\n')

    if fname is not None:
        print("tablepart '%s' written #%s" % (conversionsegment.tab.name, dividNUM))
    if conversionsegment.dimensions and conversionsegment.segment:
        jslookup = calcjslookup(conversionsegment)
        if fname is not None:
            print("javascript calculated")
        fout.write(jscode % (jslookup, dividNUM))
    
    if fname is None:
        display(HTML(fout.getvalue()))
    else:
        fout.write("</body></html>\n")
        fout.close()
        local_file = FileLink(path=os.path.basename(fname),
                              result_html_prefix="Written to file: ")
        display(local_file)
