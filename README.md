# PubChem

## 案例一
For X
    從 PubChem 網站以關鍵字 "hydroxyphenyl" 搜尋，下載 1291373 筆資料 -> hydroxyphenyl.csv
    利用 python 過濾後剩 573903 筆包含 (4-hydroxyphenyl) -> 4-hydroxyphenyl.csv
    其中 67115 筆僅包含 C H O 且不帶電 -> 1_X.csv

For Y1
    從 PubChem 網站以關鍵字 "dihydroxyphenyl" 搜尋，下載 146768 筆資料 -> dihydroxyphenyl.csv
    過濾後剩 79215 筆包含 (3,4-dihydroxyphenyl) -> 3,4-dihydroxyphenyl.csv 
    其中 32655 筆僅包含 C H O 且不帶電 -> 1_Y1.csv

For Y2
    從 PubChem 網站以關鍵字 "diol" 搜尋，下載 634847 筆資料 -> diol.csv
    過濾後剩 165698 筆包含 1,2-diol -> 1,2-diol.csv
    其中 38420 筆僅包含 C H O 且不帶電 -> 1_Y2.csv

For Z
    For Z
    將 4-hydroxyphenyl_CHO.csv 先後比對 3,4-dihydroxyphenyl_CHO.csv 和 1,2-diol_CHO.csv 的分子式，得到
    27442 筆兩者皆匹配資料 -> matchY1_matchY2.csv
        1,2:
            rescue 回 21093 筆 -> Z12_1,2.csv
            剩餘 6349 筆 -> WW12_1,2.csv
        7,8:
            rescue 回 18260 筆 -> Z12_7,8.csv
            剩餘 9182 筆 -> WW12_7,8.csv
        8,9:
            rescue 回 17744 筆 -> Z12_8,9.csv
            剩餘 9698 筆 -> WW12_8,9.csv
        11,12:
            rescue 回 14139 筆 -> Z12_11,12.csv
            剩餘 13303 筆 -> WW12_11,12.csv
        13,14:
            rescue 回 12058 筆 -> Z12_13,14.csv
            剩餘 15384 筆 -> WW12_13,14.csv
        version2:
            rescue 回 17390 筆 -> 1_Z12.csv
            剩餘 10052 筆 -> 1_WW12.csv

    22857 筆僅匹配 3,4-dihydroxyphenyl_CHO.csv -> matchY1_unmatchY2.csv
        1,2:
            rescue 回 16707 筆 -> Z1_1,2.csv
            剩餘 6150 筆 -> WW1_1,2.csv
        7,8:
            rescue 回 15717 筆 -> Z1_7,8.csv
            剩餘 7140 筆 -> WW1_7,8.csv
        8,9:
            rescue 回 15307 筆 -> Z1_8,9.csv
            剩餘 7550 筆 -> WW1_8,9.csv
        11,12:
            rescue 回 14487 筆 -> Z1_11,12.csv
            剩餘 8370 筆 -> WW1_11,12.csv
        13,14:
            rescue 回 13732 筆 -> Z1_13,14.csv
            剩餘 9125 筆 -> WW1_13,14.csv
        version2:
            rescue 回 13198 筆 -> 1_Z1.csv
            剩餘 9659 筆 -> 1_WW1.csv

    5361 筆僅匹配 1,2-diol_CHO.csv -> unmatchY1_matchY2.csv
        1,2:
            rescue 回 4641 筆 -> Z_1,2.csv
            剩餘 720 筆 -> WW_1,2.csv
        7,8:
            rescue 回 4451 筆 -> Z2_7,8.csv
            剩餘 910 筆 -> WW2_7,8.csv
        8,9:
            rescue 回 4375 筆 -> Z2_8,9.csv
            剩餘 986 筆 -> WW2_8,9.csv
        11,12:
            rescue 回 3730 筆 -> Z2_11,12.csv
            剩餘 1631 筆 -> WW2_11,12.csv
        13,14:
            rescue 回 3457 筆 -> Z2_13,14.csv
            剩餘 1904 筆 -> WW2_13,14.csv
        version2:
            rescue 回 4339 筆 -> 1_Z2.csv
            剩餘 1022 筆 -> 1_WW2.csv

    11455 筆兩者皆不匹配 -> unmatchY1_unmatchY2.csv
    

### 案例二
For X
    從 PubChem 網站以關鍵字 "dihydroxyphenyl" 搜尋，下載 146768 筆資料 -> dihydroxyphenyl.csv
    過濾後剩 79215 筆包含 (3,4-dihydroxyphenyl) -> 3,4-dihydroxyphenyl.csv 
    其中 32655 筆僅包含 C H O 且不帶電 -> 2_X.csv

For Y1
    從 PubChem 網站以關鍵字 "hydroxy and methoxyphenyl"  搜尋，下載 486719 筆資料 -> hydroxy_methoxyphenyl.csv
    過濾後剩 84714 筆包含 (4-hydroxy-3-methoxyphenyl) -> 4-hydroxy-3-methoxyphenyl.csv 
    其中 23680 筆僅包含 C H O 且不帶電 -> 2_Y1.csv

For Y2
    從 PubChem 網站以關鍵字 "hydroxy and methoxyphenyl"  搜尋，下載 486719 筆資料 -> hydroxy_methoxyphenyl.csv
    過濾後剩 32383 筆包含 (3-hydroxy-4-methoxyphenyl) -> 3-hydroxy-4-methoxyphenyl.csv 
    其中 6233 筆僅包含 C H O 且不帶電 -> 2_Y2.csv

For Z
    將 2_X.csv 先後比對 2_Y1.csv 和 2_Y2.csv 的分子式，得到
    17925 筆兩者皆匹配資料 -> 2_W12.csv
        rescue 回 15707 筆 -> 2_Z12.csv
        剩餘 2218 筆 -> 2_WW12.csv
    6961 筆僅匹配 2_Y1.csv -> 2_W1.csv
        rescue 回 6910 筆 -> 2_Z1.csv
        剩餘 51 筆 -> 2_WW1.csv
    1038 筆僅匹配 2_Y2.csv -> 2_W2.csv
        rescue 回 1038 筆 -> 2_Z2.csv
        剩餘 0 筆 -> 2_WW2.csv
    6731 筆兩者皆不匹配 -> 2_Z0.csv


### 測試階段
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
    matched.csv 中 10887 筆只含C、H、O的 -> matched_CHO_only.csv
    ummatched.csv 中 1746 筆只含C、H、O的 -> unmatched_CHO_only.csv

    從 formula_matched.csv 和 formula_unmatched.csv 中分離出僅包含C、H、O元素的分子
    matched.csv 中 10887 筆只含C、H、O的 -> matched_CHO_only.csv (matchedY1_CHO_only.csv)
    ummatched.csv 中 1746 筆只含C、H、O的 -> unmatched_CHO_only.csv (unmatchedY1_CHO_only.csv)

    比對 matchedY1_CHO_only.csv 和 1,2-diol.csv
    找到 5202 筆匹配的分子式 -> matchY1_matchY2.csv
    5685 筆未匹配的分子式 -> matchY1_unmachY2.csv

    比對 unmatchedY1_CHO_only.csv 和 1,2-diol.csv
    找到 435 筆匹配的分子式 -> unmatchY1_matchY2.csv
    1311 筆未匹配的分子式 -> unmatchY1_unmatchY2.csv