# PubChem

For X
    從 PubChem 網站以關鍵字 "hydroxyphenyl" 搜尋，下載 1291373 筆資料 -> hydroxyphenyl.csv
    利用 python 過濾後剩 573903 筆包含 (4-hydroxyphenyl) -> 4-hydroxyphenyl.csv
    其中 335700 筆無專利也無文獻 -> hydro_00.csv
    183053 筆有專利但無文獻 -> hydro_0x.csv
    55150 筆有文獻 -> hydro_xx.csv

For Y
    從 PubChem 網站以關鍵字 "dihydroxyphenyl" 搜尋，下載 146768 筆資料 -> dihydroxyphenyl.csv
    過濾後剩 79215 筆包含 (3,4-dihydroxyphenyl) -> 3,4-dihydroxyphenyl.csv
    其中 42277 筆無專利也無文獻 -> dihydro_00.csv
    25373 筆有專利但無文獻 -> dihydro_0x.csv
    11565 筆有文獻 -> dihydro_xx.csv

For Z
    比對 hydro_xx.csv 和 3,4-dihydroxyphenyl.csv
    找到 21503 筆匹配的分子式 -> formula_matched.csv
    33647 筆未匹配的分子式 -> formula_unmatched.csv


CO x6 y7 from right