Feature: Define dimension using bag.is_non_number()
    I want to be able to define a dimension by identifying all non-integer and
    non-float values in a bag.

    Scenario: Define the observations which are not measured in GBP.
        Given we load an xls file named "balanceofpayments2020q1.xls"
        And select the sheet "Records"
        And we define cell selections as
        | key             | value                                                         |  
        | percent_obs     | tab.excel_ref("C8"+":K57").is_not_number().is_not_blank()     |
        Then we confirm the cell selection contains "48" cells.
        And we confirm the cell selection is equal to:
        """
        {<I48 '(1993 Q4)'>, <K9 '(2019 Q1)'>, <K18 '(2015 Q4)'>, <K48 '(2019 Q4)'>, <I57 '(2020 Q1)'>, <K35 '(2015 Q1)'>, <I51 '(2013 Q2)'>, <E53 'Largest net asset position since 2019 Q2'>, <K38 '(2012 Q3)'>, <K45 '(2018 Q4)'>, <E50 'Largest net asset position since 2014 Q4'>, <K57 '(1970 Q3)'>, <K41 '(2019 Q1)'>, <E28 'Largest net inflow since 2019 Q4'>, <E17 'Largest deficit since 2019 Q4'>, <I12 '(2017 Q3)'>, <E24 'Largest deficit since 2019 Q4'>, <E31 'Largest net inflow since 2019 Q3'>, <I54 '(2018 Q4)'>, <E40 'Largest net disinvestment since 2019 Q2'>, <K51 '(2007 Q1)'>, <E34 'Largest net settlement receipts since 2019 Q3'>, <K29 '(2014 Q1)'>, <E56 'Largest net asset position recorded '>, <I35 '(2008 Q1)'>, <E14 'Largest deficit since 2016 Q2'>, <I38 '(2015 Q1)'>, <K32 '(2008 Q4)'>, <I21 '(1981 Q1)'>, <E11 'Largest surplus since 2018 Q3'>, <K12 '(1965 Q3)'>, <I18 '(1982 Q1)'>, <I32 '(2012 Q3)'>, <E20 'Largest deficit since 2019 Q3'>, <K15 '(2015 Q4)'>, <I15 '(2005 Q2)'>, <E47 'Largest net liability position since 2019 Q4'>, <K54 '(2007 Q4)'>, <I41 '(2018 Q4)'>, <K21 '(2019 Q1)'>, <I29 '(2000 Q1)'>, <I25 '(2007 Q4)'>, <E44 'Largest net liability position since 2019 Q4'>, <I45 '(2008 Q4)'>, <E8 'Largest deficit since 2019 Q3'>, <K25 '(2006 Q2)'>, <E37 'Largest net investment since 2018 Q4'>, <I9 '(1981 Q1)'>}
        """
  