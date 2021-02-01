Feature: Define a dimension as a range of values from a cell reference but only including the cells containing whitespace.
  I want to be able to define a dimension as a range of values from a cell reference, but I want to
  ignore any cells containing values that lie within that range.

  Scenario: Define whitespace year from a range of cell references ignoring any value-containing cells.
    Given we load an xls file named "bulletindataset2v2.xls"
    And select the sheet "Table 2a"
    And we define cell selections as
      | key             | value                                         |  
      | unit            | tab.excel_ref("A11:A250").is_whitespace()     |
    Then we confirm year contains no value storing cells.
    And we confirm the cell selection contains "182" cells.
    And we confirm the cell selection is equal to:
    """
    {<A104 ''>, <A62 ''>, <A97 ''>, <A170 ''>, <A179 ''>, <A102 ''>, <A60 ''>, <A120 ''>, <A177 ''>, <A100 ''>, <A58 ''>, <A77 ''>, <A118 ''>, <A191 ''>, <A136 ''>, <A116 ''>, <A93 ''>, <A134 ''>, <A82 ''>, <A110 ''>, <A132 ''>, <A96 ''>, <A57 ''>, <A108 ''>, <A34 ''>, <A106 ''>, <A48 ''>, <A37 ''>, <A113 ''>, <A194 ''>, <A53 ''>, <A72 ''>, <A208 ''>, <A70 ''>, <A169 ''>, <A68 ''>, <A215 ''>, <A45 ''>, <A227 ''>, <A213 ''>, <A232 ''>, <A225 ''>, <A230 ''>, <A188 ''>, <A239 ''>, <A50 ''>, <A248 ''>, <A228 ''>, <A186 ''>, <A205 ''>, <A64 ''>, <A131 ''>, <A246 ''>, <A203 ''>, <A129 ''>, <A244 ''>, <A221 ''>, <A105 ''>, <A143 ''>, <A210 ''>, <A152 ''>, <A219 ''>, <A224 ''>, <A150 ''>, <A185 ''>, <A236 ''>, <A162 ''>, <A126 ''>, <A148 ''>, <A167 ''>, <A234 ''>, <A176 ''>, <A243 ''>, <A137 ''>, <A124 ''>, <A165 ''>, <A241 ''>, <A183 ''>, <A122 ''>, <A140 ''>, <A181 ''>, <A200 ''>, <A158 ''>, <A65 ''>, <A138 ''>, <A147 ''>, <A198 ''>, <A156 ''>, <A88 ''>, <A145 ''>, <A196 ''>, <A173 ''>, <A86 ''>, <A121 ''>, <A159 ''>, <A98 ''>, <A171 ''>, <A84 ''>, <A61 ''>, <A112 ''>, <A73 ''>, <A101 ''>, <A78 ''>, <A192 ''>, <A153 ''>, <A76 ''>, <A117 ''>, <A94 ''>, <A135 ''>, <A74 ''>, <A233 ''>, <A92 ''>, <A133 ''>, <A81 ''>, <A90 ''>, <A109 ''>, <A40 ''>, <A38 ''>, <A114 ''>, <A56 ''>, <A36 ''>, <A128 ''>, <A195 ''>, <A54 ''>, <A89 ''>, <A193 ''>, <A52 ''>, <A207 ''>, <A69 ''>, <A216 ''>, <A46 ''>, <A249 ''>, <A44 ''>, <A212 ''>, <A231 ''>, <A42 ''>, <A189 ''>, <A240 ''>, <A201 ''>, <A229 ''>, <A187 ''>, <A206 ''>, <A49 ''>, <A247 ''>, <A204 ''>, <A245 ''>, <A222 ''>, <A144 ''>, <A211 ''>, <A220 ''>, <A209 ''>, <A151 ''>, <A218 ''>, <A237 ''>, <A163 ''>, <A223 ''>, <A149 ''>, <A168 ''>, <A235 ''>, <A161 ''>, <A125 ''>, <A175 ''>, <A242 ''>, <A184 ''>, <A164 ''>, <A141 ''>, <A182 ''>, <A217 ''>, <A66 ''>, <A139 ''>, <A180 ''>, <A199 ''>, <A157 ''>, <A80 ''>, <A41 ''>, <A146 ''>, <A197 ''>, <A155 ''>, <A174 ''>, <A160 ''>, <A172 ''>, <A85 ''>}
    """    
