import pandas as pd
import re

# --- 加 O 函式 ---
def add_oxygen(formula):
    o_index = formula.find('O')
    if o_index == -1:
        return formula + 'O1'
    after_o = formula[o_index+1:]
    match = re.match(r'(\d+)', after_o)
    if match:
        number = int(match.group(1)) + 1
        return formula[:o_index] + f"O{number}" + after_o[match.end():]
    else:
        return formula[:o_index+1] + "1" + after_o

# --- 載入資料 ---
x_file = "unmatchY1.csv"
y_file = "1,2-diol_CHO.csv"

df_x = pd.read_csv(x_file)
df_y = pd.read_csv(y_file)

# --- 建立 Y 的公式對 CID 的查表字典 ---
y_formula_to_cid = dict(zip(df_y["Molecular_Formula"], df_y["Compound_CID"]))

# --- 加一個 O 並建立 Modified_Formula 欄位 ---
# df_x["Modified_Formula"] = df_x["Molecular_Formula"].apply(add_oxygen)

# --- 對應 Y 中的 CID（有則記錄，無則 NaN）---
df_x["Matched_Y_CID"] = df_x["Modified_Formula"].map(y_formula_to_cid)

# --- 分割成兩份 ---
df_unmatched = df_x[df_x["Matched_Y_CID"].isna()]      # 沒對到的
df_matched   = df_x[df_x["Matched_Y_CID"].notna()]     # 有對到的

# --- 輸出檔案 ---
df_unmatched.to_csv("unmatchY1_unmatchY2.csv", index=False)
df_matched.to_csv("unmatchY1_matchY2.csv", index=False)

# --- 統計結果 ---
print(f"❌ 未匹配數量：{len(df_unmatched)} → unmatchY1_unmatchY2.csv")
print(f"✅ 已匹配數量：{len(df_matched)}   → unmatchY1_matchY2.csv")