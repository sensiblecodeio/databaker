# encoding: utf-8
# HTML preview of the dimensions and table (will be moved to a function in databakersolo)

import io, os, collections, re, warnings, csv, datetime
import databaker.constants
from databaker.jupybakeutils import ConversionSegment
template = databaker.constants.template

try:   import pandas
except ImportError:  pandas = None  # no pandas in pypy

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



def Lyield_dimension_values(dval, isegmentnumber, Cheaderadditionals):
    for k in template.headermeasurements:
        if isinstance(k, tuple):
            yield dval.get(k[1], '')
        elif k == template.conversionsegmentnumbercolumn:
            yield isegmentnumber
        else:
            yield ''
            
    for dlab in Cheaderadditionals:
        for k in template.headeradditionals:
            if isinstance(k, tuple):
                if k[1] == "NAME":
                    yield dlab
                else:
                    assert k[1] == "VALUE"
                    yield dval[dlab]
            else:
                yield ''


def writetechnicalCSV(outputfile, conversionsegments):
    "Output the CSV into the bloated WDA format (takes lists of conversionsegments or pandas tables)"
    if not isinstance(conversionsegments, (list, tuple)):
        conversionsegments = [ conversionsegments ]
        
    if outputfile is not None:
        print("writing %d conversion segments into %s" % (len(conversionsegments), os.path.abspath(outputfile)))
        try:
            filehandle = open(outputfile, "w", newline='\n', encoding='utf-8')
        except TypeError:  # this happens if you run in pypy2 because the newline parameter is not recognized
            filehandle = open(outputfile, "w")
    else:
        filehandle = io.StringIO()  # to return as string for print preview perhaps
    csv_writer = csv.writer(filehandle)
    row_count = 0
        
    for isegmentnumber, conversionsegment in enumerate(conversionsegments):
        if isegmentnumber == 0:   # only first segment gets a CSV header for the whole file (even if it is not consistent for the remaining segments)
            if isinstance(conversionsegment, ConversionSegment):
                Cheaderadditionals = [ dimension.label  for dimension in conversionsegment.dimensions  if dimension.label not in template.headermeasurementnamesSet ]
                assert len(Cheaderadditionals) == conversionsegment.numheaderadditionals
            elif pandas is not None:
                assert isinstance(conversionsegment, pandas.DataFrame), "function takes only ConversionSegments of pandas.DataFrames"
                if not isinstance(conversionsegment.index, pandas.RangeIndex):
                    conversionsegment = conversionsegment.reset_index()  # in case of playing around with indexes
                Cheaderadditionals = [colname  for colname in conversionsegment.columns  if colname not in template.headermeasurementnamesSet and colname[:2] != "__"]
            csv_writer.writerow(HLDUPgenerate_header_row(len(Cheaderadditionals)))

        if isinstance(conversionsegment, ConversionSegment):
            timeunitmessage = ""
            if conversionsegment.processedrows is None: 
                timeunitmessage = conversionsegment.process()  

            if outputfile is not None:
                print("conversionwrite segment size %d table '%s'; %s" % (len(conversionsegment.processedrows), conversionsegment.tab.name, timeunitmessage))
            for row in conversionsegment.processedrows:
                csv_writer.writerow(Lyield_dimension_values(row, isegmentnumber, Cheaderadditionals))
                row_count += 1

        else:  # pandas.Dataframe case
            assert pandas is not None
            if outputfile is not None:
                print("pdconversionwrite segment size %d" % (len(conversionsegment)))
            for i in range(len(conversionsegment)):  # quick and dirty to use same dict-based function
                csv_writer.writerow(Lyield_dimension_values(dict(conversionsegment.iloc[i].dropna()), isegmentnumber, Cheaderadditionals))
                row_count += 1

    csv_writer.writerow(["*"*9, row_count])
    if outputfile is not None:
        filehandle.close()
    else:
        return filehandle.getvalue()



def readtechnicalCSV(wdafile, bverbose=False, baspandas=True):
    if baspandas and pandas is None:
        baspandas = False
        
    "Read a WDA CSV back from its file into an lookup table from segment number to (each a list of dicts)"
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
        
    wdasegments = { }             # { segmentnumber: ( [ data_dicts ], [ordered_header_list] ) }
    previsegmentnumber = None
    segmentheaderssegmentL = [ ]  # [ [ordered_header_list] ]
    
    for row in wdain:
        if row[0] == '*********':
            nrows = sum(len(wdasegment)  for wdasegment, segmentheaders in wdasegments.values())
            if int(row[1]) != nrows:
                warnings.warn("row number doesn't match %d should be %d" % (int(row[1]), nrows))
            assert len(list(wdain)) == 0, "***** must be on last row"
            break

        dval = { }
        isegmentnumber = None
        for r, k in zip(row, template.headermeasurements):
            if isinstance(k, tuple):
                nk = k[1]
                if r:
                    assert nk not in dval or dval[nk] == r
                    dval[nk] = r
                else:
                    assert not dval.get(nk)
            elif k == template.conversionsegmentnumbercolumn and r:
                isegmentnumber = int(r)
            else:
                assert not r
                
        lnumheaderadditionals = (len(row) - len(template.headermeasurements))
        assert lnumheaderadditionals % len(template.headeradditionals) == 0
        numheaderadditionals = lnumheaderadditionals//len(template.headeradditionals)
        
        segmentheaderssegmentJ = [ ]  
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
            segmentheaderssegmentJ.append(rname)
                
        if isegmentnumber is None:
            if not segmentheaderssegmentL or segmentheaderssegmentL[-1] != segmentheaderssegmentJ:
                segmentheaderssegmentL.append(segmentheaderssegmentJ)
            isegmentnumber = len(segmentheaderssegmentL) - 1
        elif isegmentnumber in wdasegments:
            assert wdasegments[isegmentnumber][1] == segmentheaderssegmentJ
                
        if isegmentnumber not in wdasegments:
            if bverbose and previsegmentnumber is not None:
                print("segment %d loaded with %d rows" % (previsegmentnumber, len(wdasegments[previsegmentnumber][0])))
            wdasegments[isegmentnumber] = ([ ], segmentheaderssegmentJ)
            
        wdasegments[isegmentnumber][0].append(dval)
        previsegmentnumber = isegmentnumber
    if bverbose and previsegmentnumber is not None:
        print("segment %d loaded with %d rows" % (previsegmentnumber, len(wdasegments[previsegmentnumber][0])))
    filehandle.close()
    
    if not baspandas:
        return [ wdasegment  for wdasegment, segmentheaders in wdasegments.values() ]
    
    res = [ ]
    for wdasegment, segmentheaders in wdasegments.values():
        df = pandas.DataFrame.from_dict(wdasegment)
        
        # sort the columns (problem with using from_dict)
        dfcols = list(df.columns)
        newdfcols = [ ]
        for k in template.headermeasurements:
            if isinstance(k, tuple):
                if k[1] in dfcols:
                    newdfcols.append(k[1])
                    dfcols.remove(k[1])
        for segmentheader in segmentheaders:
            assert segmentheader in dfcols
            newdfcols.append(segmentheader)
            dfcols.remove(segmentheader)
        assert not dfcols, ("unexplained extra columns", dfcols)
        
        res.append(df[newdfcols])   # map the new column list in
    return res
        