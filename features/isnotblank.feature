Feature: Define a dimension as a range of values from a cell reference but not including the blank cells.
  I want to be able to define a dimension as a range of values from a cell reference, but I want to
  ignore any blank cells that lie within that range.

  Scenario: Define year from a range of cell references ignoring any blank cells.
    Given we load an xls file named "bulletindataset2v2.xls"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define year as the non-blank values in cells "A11:A250"
    Then we confirm year contains no blank cells.

Scenario: Define year as correct cells.
    Given we load an xls file named "bulletindataset2v2.xls"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define year as the non-blank values in cells "A11:A250" 
    Then we confirm that year without blanks is equal to:
    """
    {<A18 2004.0>, <A23 2009.0>, <A27 2013.0>, <A15 2001.0>, <A202 2016.0>, <A91 2011.0>, <A115 2017.0>, <A67 2005.0>, <A123 2019.0>, <A32 2018.0>, <A33 2019.0>, <A127 2020.0>, <A166 2013.0>, <A28 2014.0>, <A51 2001.0>, <A43 1999.0>, <A238 2019.0>, <A22 2008.0>, <A26 2012.0>, <A59 2003.0>, <A79 2008.0>, <A14 2000.0>, <A31 2017.0>, <A130 2010.0>, <A154 2012.0>, <A75 2007.0>, <A250 2020.0>, <A111 2016.0>, <A21 2007.0>, <A107 2015.0>, <A119 2018.0>, <A214 2017.0>, <A17 2003.0>, <A39 1998.0>, <A142 2011.0>, <A13 1999.0>, <A30 2016.0>, <A55 2002.0>, <A103 2014.0>, <A20 2006.0>, <A71 2006.0>, <A25 2011.0>, <A83 2009.0>, <A35 1997.0>, <A87 2010.0>, <A47 2000.0>, <A12 1998.0>, <A226 2018.0>, <A19 2005.0>, <A11 1997.0>, <A190 2015.0>, <A63 2004.0>, <A99 2013.0>, <A95 2012.0>, <A24 2010.0>, <A16 2002.0>, <A178 2014.0>, <A29 2015.0>}
    """    
