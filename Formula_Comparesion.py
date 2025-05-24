import pandas as pd
import re

# # --- 加 O 函式 ---
# def add_oxygen(formula):
#     o_index = formula.find('O')
#     if o_index == -1:
#         return formula + 'O1'
#     after_o = formula[o_index+1:]
#     match = re.match(r'(\d+)', after_o)
#     if match:
#         number = int(match.group(1)) + 1
#         return formula[:o_index] + f"O{number}" + after_o[match.end():]
#     else:
#         return formula[:o_index+1] + "1" + after_o

def add_C1H2(formula):
    # 處理 C
    c_index = formula.find('C')
    if c_index == -1:
        formula += 'C1'
    else:
        after_c = formula[c_index+1:]
        match = re.match(r'(\d+)', after_c)
        if match:
            number = int(match.group(1)) + 1
            formula = formula[:c_index] + f"C{number}" + after_c[match.end():]
        else:
            formula = formula[:c_index+1] + '1' + after_c

    # 處理 H（注意 formula 可能已改變，要重新找 H）
    h_index = formula.find('H')
    if h_index == -1:
        formula += 'H2'
    else:
        after_h = formula[h_index+1:]
        match = re.match(r'(\d+)', after_h)
        if match:
            number = int(match.group(1)) + 2
            formula = formula[:h_index] + f"H{number}" + after_h[match.end():]
        else:
            formula = formula[:h_index+1] + '2' + after_h

    return formula

# --- 載入資料 ---
x_file = "matchY1.csv"
y_file = "3-hydroxy-4-methoxyphenyl_CHO.csv"

df_x = pd.read_csv(x_file)
df_y = pd.read_csv(y_file)

# --- 建立 Y 的公式對 CID 的查表字典 ---
y_formula_to_cid = dict(zip(df_y["Molecular_Formula"], df_y["Compound_CID"]))

# --- 加 C1H2 並建立 Modified_Formula 欄位 ---
#df_x["Modified_Formula"] = df_x["Molecular_Formula"].apply(add_C1H2)

# --- 對應 Y 中的 CID（有則記錄，無則 NaN）---
df_x["Matched_Y_CID"] = df_x["Modified_Formula"].map(y_formula_to_cid)

# --- 分割成兩份 ---
df_unmatched = df_x[df_x["Matched_Y_CID"].isna()]      # 沒對到的
df_matched   = df_x[df_x["Matched_Y_CID"].notna()]     # 有對到的

# --- 輸出檔案 ---
df_unmatched.to_csv("matchY1_unmatchY2.csv", index=False)
df_matched.to_csv("matchY1_matchY2.csv", index=False)

# --- 統計結果 ---
print(f"❌ 未匹配數量：{len(df_unmatched)} → matchY1_unmatchY2.csv")
print(f"✅ 已匹配數量：{len(df_matched)}   → matchY1_matchY2.csv")