# PubChem

For X
    從 PubChem 網站以關鍵字 "hydroxyphenyl" 搜尋，下載 1291373 筆資料 -> hydroxyphenyl.csv
    利用 python 過濾後剩 573903 筆包含 (4-hydroxyphenyl) -> 4-hydroxyphenyl.csv
    其中 335700 筆無專利也無文獻 -> hydro_00.csv
    183053 筆有專利但無文獻 -> hydro_0x.csv
    55150 筆有文獻 -> hydro_xx.csv

For Y1
    從 PubChem 網站以關鍵字 "dihydroxyphenyl" 搜尋，下載 146768 筆資料 -> dihydroxyphenyl.csv
    過濾後剩 79215 筆包含 (3,4-dihydroxyphenyl) -> 3,4-dihydroxyphenyl.csv
    其中 42277 筆無專利也無文獻 -> dihydro_00.csv
    25373 筆有專利但無文獻 -> dihydro_0x.csv
    11565 筆有文獻 -> dihydro_xx.csv

For Y2
    從 PubChem 網站以關鍵字 "diol" 搜尋，下載 634847 筆資料 -> diol.csv
    過濾後剩 165698 筆包含 1,2-diol -> 1,2-diol.csv
    其中 85388 筆無專利也無文獻 -> diol_00.csv
    71234 筆有專利但無文獻 -> diol_0x.csv
    9076 筆有文獻 -> diol_xx.csv

For Z
    比對 hydro_xx.csv 和 3,4-dihydroxyphenyl.csv
    找到 21503 筆匹配的分子式 -> formula_matched.csv
    33647 筆未匹配的分子式 -> formula_unmatched.csv

    從 formula_matched.csv 和 formula_unmatched.csv 中分離出僅包含C、H、O元素的分子
    matched.csv 中 10887 筆只含C、H、O的 -> matched_CHO_only.csv (matchedY1_CHO_only.csv)
    ummatched.csv 中 1746 筆只含C、H、O的 -> unmatched_CHO_only.csv (unmatchedY1_CHO_only.csv)

    比對 matchedY1_CHO_only.csv 和 1,2-diol.csv
    找到 5202 筆匹配的分子式 -> matchY1_matchY2.csv
    5685 筆未匹配的分子式 -> matchY1_unmachY2.csv

    比對 unmatchedY1_CHO_only.csv 和 1,2-diol.csv
    找到 435 筆匹配的分子式 -> unmatchY1_matchY2.csv
    1311 筆未匹配的分子式 -> unmatchY1_unmatchY2.csv

CO x6 y7 from right