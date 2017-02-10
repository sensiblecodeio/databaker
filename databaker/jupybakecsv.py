# encoding: utf-8
# HTML preview of the dimensions and table (will be moved to a function in databakersolo)
from __future__ import unicode_literals, division

import six
import io, os, collections, re, warnings, csv, datetime
import databaker.constants
from databaker.jupybakeutils import ConversionSegment
template = databaker.constants.template

def HLDUPgenerate_header_row(numheaderadditionals):
    res = [ (k[0] if isinstance(k, tuple) else k)  for k in template.headermeasurements ]
    for i in range(numheaderadditionals):
        for k in template.headeradditionals:
            if isinstance(k, tuple):
                sk = k[0]
            else:
                sk = k
            res.append("%s_%d" % (sk, i+1))
    return res


# new version of write CSV
def writetechnicalCSV(outputfile, conversionsegments):
    if type(conversionsegments) is ConversionSegment:
        conversionsegments = [conversionsegments]
        
    if outputfile is not None:
        print("writing %d conversion segments into %s" % (len(conversionsegments), os.path.abspath(outputfile)))
        filehandle = open(outputfile, "w", newline='\n', encoding='utf-8')
    else:
        filehandle = io.StringIO()
    csv_writer = csv.writer(filehandle)
    row_count = 0
        
    for isegmentnumber, conversionsegment in enumerate(conversionsegments):
        if isegmentnumber == 0:   # only first segment
            csv_writer.writerow(HLDUPgenerate_header_row(conversionsegment.numheaderadditionals))
            
        timeunitmessage = ""
        if conversionsegment.processedrows is None: 
            timeunitmessage = conversionsegment.process()  

        if outputfile is not None:
            print("conversionwrite segment size %d table '%s; %s" % (len(conversionsegment.processedrows), conversionsegment.tab.name, timeunitmessage))
        for row in conversionsegment.processedrows:
            csv_writer.writerow(conversionsegment.Lyield_dimension_values(row, isegmentnumber))
            row_count += 1
            
    csv_writer.writerow(["*"*9, row_count])
    if outputfile is not None:
        filehandle.close()
    else:
        return filehandle.getvalue()



def readtechnicalCSV(wdafile, bverbose=False):
    if isinstance(wdafile, str):
        if len(wdafile) > 200 and '\n' in wdafile:
            filehandle = io.StringIO(wdafile)
        else:
            filehandle = open(wdafile, "r", encoding='utf-8')
    else:
        assert isinstance(wdafile, io.StringIO)
        filehandle = wdafile
        
    wdain = csv.reader(filehandle)
    # First check that the headers are what we expect
    wdaheaders = wdain.__next__()
    numheaderadditionals = (len(wdaheaders) - len(template.headermeasurements))//len(template.headeradditionals)
    if not (wdaheaders == HLDUPgenerate_header_row(numheaderadditionals)):
        print("WDA heades don't match.  nothing is likely to work now")
        
    wdasegments = { }
    previsegmentnumber = None
    for row in wdain:
        if row[0] == '*********':
            nrows = sum(map(len, wdasegments.values()))
            assert int(row[1]) == nrows, ("row number doesn't match", int(row[1]), nrows)
            assert len(list(wdain)) == 0
            break

        dval = { }
        isegmentnumber = None
        for r, k in zip(row, template.headermeasurements):
            if isinstance(k, tuple):
                nk = template.headermeasurementnumvalues[k[1]]
                if r:
                    assert nk not in dval or dval[nk] == r
                    dval[nk] = r
                else:
                    assert not dval.get(nk)
            elif k == template.conversionsegmentnumbercolumn:
                isegmentnumber = int(r or '0')
            else:
                assert not r
                
            lnumheaderadditionals = (len(row) - len(template.headermeasurements))
            assert lnumheaderadditionals % len(template.headeradditionals) == 0
            numheaderadditionals = lnumheaderadditionals//len(template.headeradditionals)
            for i in range(numheaderadditionals):
                rname, rvalue = None, None
                i0 = len(template.headermeasurements) + i*len(template.headeradditionals)
                for r, k in zip(row[i0:i0+len(template.headeradditionals)], template.headeradditionals):
                    if isinstance(k, tuple):
                        if k[1] == "NAME":
                            assert rname is None or rname == r, (rname, r)
                            rname = r
                        else:
                            assert k[1] == "VALUE"
                            assert rvalue is None or rvalue == r
                            rvalue = r
                    else:
                        assert not r
                assert rname, (rname, dval, row)
                dval[rname] = rvalue
                
        if isegmentnumber not in wdasegments:
            if bverbose and previsegmentnumber is not None:
                print("segment %d loaded with %d rows" % (previsegmentnumber, len(wdasegments[previsegmentnumber])))
            wdasegments[isegmentnumber] = [ ]
            
        wdasegments[isegmentnumber].append(dval)
        previsegmentnumber = isegmentnumber
    if bverbose and previsegmentnumber is not None:
        print("segment %d loaded with %d rows" % (previsegmentnumber, len(wdasegments[previsegmentnumber])))
    filehandle.close()
    return wdasegments


# separated out so we can decide the severity of them before printing them out
wdamsgstrings = { 
    "WDAHEADERSINCONSISTENT": "Inconsistent extra headings headings in segment: %s", 
    "WDAHEADERSMISSING": "Extra headings in segment than in wda file: %s", 
    "WDAHEADERSEXTRA": "Extra headings in wda file not in segment: %s", 
    "WDACOLUMNNOTCONSTANT": "Constant column %s has multiple values: %s", 
    "WDACOLUMNCONSTCHANGED": "Constant column %s value changed %s but was in wda file %s", 
    "NEWVALUESINSEGMENT": "Unmatched new values in segment %s", 
    "WDAEXTRAVALUES": "Unmatched extra values in wda file %s", 
    "WDADUPLICATESMISMATCH": "Duplicates mismatch counts %s", 
    "EXTRAWDACONVERSIONSEGMENTS": "Extra conversion segments in wda file %s",
}

def headersfromwdasegment(wdaseg, msglist):
    derivedheaders = [ databaker.constants.OBS ] + (template.SH_Create_ONS_time and [ databaker.constants.TIMEUNIT ] or []) + (databaker.constants.DATAMARKER and [databaker.constants.DATAMARKER] or [])
    headersunion = None
    headersintersection = None
    for wdarow in wdaseg:
        ahset = set(k  for k in wdarow.keys()  if k not in derivedheaders)
        if headersunion is None:
            headersintersection = set(ahset)
            headersunion = set(ahset)
        else:
            headersunion.update(ahset)
            headersintersection.intersection_update(ahset)
    if headersunion != headersintersection:
        msglist.append(("WDAHEADERSINCONSISTENT", headersunion.difference(headersintersection)))
    return headersintersection

def extraheaderscheck(conversionsegment, wdaseg, msglist):
    wdaheaders = headersfromwdasegment(wdaseg, msglist)
    segmentheaders = set([c.label  for c in conversionsegment.dimensions])
    extraheadersinsegment = segmentheaders.difference(wdaheaders)
    extraheadersinwdaseg = wdaheaders.difference(segmentheaders)
    if extraheadersinsegment:
        msglist.append(("WDAHEADERSMISSING", extraheadersinsegment))
    if extraheadersinwdaseg:
        msglist.append(("WDAHEADERSEXTRA", extraheadersinwdaseg))
    return wdaheaders.intersection(segmentheaders)

def checktheconstantdimensions(conversionsegment, headers, wdaseg, msglist):
    for dimension in conversionsegment.dimensions:
        if dimension.label in headers:
            if dimension.hbagset is None:
                constval = dimension.cellvalueoverride.get(None)
                wdaconst = set(row.get(dimension.label)  for row in wdaseg)
                if len(wdaconst) != 1:
                    msglist.append(("WDACOLUMNNOTCONSTANT", (dimension.label, wdaconst)))
                elif constval not in wdaconst:
                    msglist.append(("WDACOLUMNCONSTCHANGED", (dimension.label, constval, wdaconst.pop())))
                headers.remove(dimension.label)
    return headers

def checksegmentobsvalues(processedrows, headers, wdaseg, msglist):
    oheaders = [databaker.constants.OBS]+list(headers)

    # produce counts of each element in case there are duplicates (we are not keeping the orders of the lists)
    ccounts = collections.Counter(tuple(row.get(h)  for h in oheaders)  for row in processedrows)
    wcounts = collections.Counter(tuple(wrow.get(h)  for h in oheaders)  for wrow in wdaseg)
    cset = set(ccounts.keys())
    wset = set(wcounts.keys())
    
    cdiffextra = cset.difference(wset)
    sdiffextra = wset.difference(cset)
    if cdiffextra:
        msglist.append(("NEWVALUESINSEGMENT", cdiffextra))
    if sdiffextra:
        msglist.append(("WDAEXTRAVALUES", sdiffextra))
        
    dupmismatch = { }
    for s in cset.intersection(wset):
        if ccounts[s] != wcounts[s]:
            dupmismatch[s] = (ccounts[s], wcounts[s])
    if dupmismatch:
        msglist.append(("WDADUPLICATESMISMATCH", dupmismatch))


def CompareConversionSegments(conversionsegments, wdafile, bprintwarnings):
    bverbose = True
    if type(conversionsegments) is ConversionSegment:
        conversionsegments = [conversionsegments]
    
    msglistperseg = { }
    wdasegs = readtechnicalCSV(wdafile, bverbose)
    extracsegs = [ c  for c in wdasegs.keys()  if not 0<=c<len(conversionsegments) ]
    if extracsegs:
        msglistperseg[-1] = [ ("EXTRAWDACONVERSIONSEGMENTS", extracsegs) ]
    for isegmentnumber, conversionsegment in enumerate(conversionsegments):
        
        if conversionsegment.processedrows is None: 
            timeunitmessage = conversionsegment.process()  
            print("conversionwrite segment size %d table '%s; %s" % (len(conversionsegment.processedrows), conversionsegment.tab.name, timeunitmessage))
        
        msglist = [ ]
        wdaseg = wdasegs[isegmentnumber]
        headers = extraheaderscheck(conversionsegment, wdaseg, msglist)
        headers = checktheconstantdimensions(conversionsegment, headers, wdaseg, msglist)
        checksegmentobsvalues(conversionsegment.processedrows, headers, wdaseg, msglist)
        if msglist:
            msglistperseg[isegmentnumber] = msglist
            
    if bprintwarnings:
        for isegmentnumber, msglist in msglistperseg.items():
            for msg, v in msglist:
                print("Conversion seg %d error: %s" % (isegmentnumber, (wdamsgstrings[msg] % v)))

    return msglistperseg

