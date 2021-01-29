Feature: Define dimension using bag.is_number()
    I want to be able to define a dimension by identifying all integer and
    float values in a bag.

    Scenario: Define the observations which are measured in GBP.
    Given we load an xls file named "balanceofpayments2020q1.xls"

    And select the sheet "Records"

    And we define cell selections as
      | key             | value                                                        |  
      | no_percent_obs     | tab.excel_ref("C8"+":K57").is_number().is_not_blank()     |

    Then we confirm the cell selection contains "48" cells.

Scenario: Define the observations as correct the cells.
    Given we load an xls file named "balanceofpayments2020q1.xls"

    And select the sheet "Records"

    And we define cell selections as
      | key             | value                                                        |  
      | no_percent_obs     | tab.excel_ref("C8"+":K57").is_number().is_not_blank()     |

    Then we confirm the cell selection is equal to:
    """
    {<I37 133.4>, <C56 137.2>, <K44 -112.1>, <K31 -191.4>, <I14 7.7>, <C28 -2.0>, <K53 -387.5>, <I28 98.5>, <C34 18.7>, <I17 0.3>, <C53 280.7>, <K20 -35.8>, <I34 63.3>, <K37 -141.9>, <I31 121.0>, <I20 2.7>, <I44 494.2>, <K50 -37.6>, <I8 1.6>, <C40 -3.3>, <C24 -0.1>, <I40 13.1>, <C37 42.1>, <C47 -821.8>, <C20 -21.1>, <K8 -49.4>, <C14 -13.6>, <I50 163.3>, <C17 -6.3>, <I56 137.2>, <C11 28.1>, <I47 143.1>, <K34 -96.8>, <K28 -139.7>, <K24 -1.6>, <K11 0.0>, <I11 28.8>, <C8 -29.3>, <K47 -891.8>, <K17 -7.4>, <K14 -18.4>, <K40 -6.3>, <C31 -50.4>, <I24 0.5>, <C44 -53.8>, <I53 525.0>, <K56 1.1>, <C50 70.7>}
    """    