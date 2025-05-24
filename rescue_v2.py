# import pandas as pd
# import re

# # 保留 C 和 O
# def filter_smile_CO_only(smile):
#     return ''.join(re.findall(r'[CO]', str(smile)))

# def main():
#     # 讀入兩個檔案
#     df1 = pd.read_csv("2_Y1.csv")
#     df2 = pd.read_csv("2_Y2.csv")

#     # 過濾 SMILES，只保留 C/O
#     df1["Filtered_SMILES"] = df1["SMILES"].apply(filter_smile_CO_only)
#     df2["Filtered_SMILES"] = df2["SMILES"].apply(filter_smile_CO_only)

#     # 過濾開頭為 COC
#     df1 = df1[df1["Filtered_SMILES"].str.startswith("COC")]
#     df2 = df2[df2["Filtered_SMILES"].str.startswith("COC")]

#     # 取得交集的 filtered_smiles
#     set1 = set(df1["Filtered_SMILES"])
#     set2 = set(df2["Filtered_SMILES"])
#     intersection = set1 & set2

#     # 只保留交集部分
#     df_common = df1[df1["Filtered_SMILES"].isin(intersection)].copy()

#     # 建立輸出欄位
#     df_common["Trimmed_SMILES"] = df_common["Filtered_SMILES"].str[2:]  # 移除開頭 CO

#     # 輸出欄位選擇
#     df_output = df_common[["Molecular_Formula", "Trimmed_SMILES"]]

#     # 輸出
#     df_output.to_csv("2_Y.csv", index=False)
#     print(f"✅ 已完成，共輸出 {len(df_output)} 筆資料至 2_Y.csv")

# if __name__ == "__main__":
#     main()




# import pandas as pd
# import re
# from collections import defaultdict

# # 只保留 C 和 O
# def filter_smile_CO_only(smile):
#     return ''.join(re.findall(r'[CO]', str(smile)))

# # 讀取檔案
# df_x = pd.read_csv("2_W1.csv")  # 含 Modified_Formula 和 SMILES
# df_y = pd.read_csv("2_Y.csv")   # 含 Molecular_Formula 和 Trimmed_SMILES

# # 建立 Y 的 mapping：Molecular_Formula → [Trimmed_SMILES]
# y_map = defaultdict(set)
# for _, row in df_y.iterrows():
#     mf = row["Molecular_Formula"]
#     ts = row["Trimmed_SMILES"]
#     if pd.notna(mf) and pd.notna(ts):
#         y_map[mf].add(ts)

# # 處理 X 檔案
# matched_rows = []
# unmatched_rows = []

# for _, row in df_x.iterrows():
#     modified_formula = row["Modified_Formula"]
#     x_smile = row["SMILES"]

#     if pd.isna(modified_formula) or pd.isna(x_smile):
#         continue

#     x_filtered = filter_smile_CO_only(x_smile)
#     match_found = x_filtered in y_map.get(modified_formula, set())

#     new_row = row.copy()
#     new_row["Filtered_SMILES_X"] = x_filtered

#     if match_found:
#         matched_rows.append(new_row)
#     else:
#         unmatched_rows.append(new_row)

# # 輸出結果
# pd.DataFrame(matched_rows).to_csv("2_WW1.csv", index=False)
# pd.DataFrame(unmatched_rows).to_csv("2_Z1.csv", index=False)

# print("✅ 輸出完成：")
# print(f"2_WW1.csv 資料量：{len(matched_rows)} 筆")
# print(f"2_Z1.csv 資料量：{len(unmatched_rows)} 筆")

import pandas as pd
import re
from collections import defaultdict

# --- 過濾 SMILES，只保留 C 和 O ---
def filter_smile_CO_only(smile):
    return ''.join(re.findall(r'[CO]', str(smile)))

# --- 比對邏輯：X 比 Y 多一個 O，從 X 中移除一個 O 看是否等於 Y ---
def is_match_by_removing_one_O_from_X(x_filtered, y_trimmed):
    if len(x_filtered) != len(y_trimmed) + 1:
        return False
    for i, c in enumerate(x_filtered):
        if c == 'O':
            candidate = x_filtered[:i] + x_filtered[i+1:]
            if candidate == y_trimmed:
                return True
    return False

def main():
    # 📥 輸入檔案
    x_file = "2_W12.csv"   # 含 Modified_Formula 和 SMILES
    y_file = "2_Y.csv"    # 含 Molecular_Formula 和 Trimmed_SMILES

    # 📤 輸出檔案
    out_match = "2_WW12.csv"
    out_unmatch = "2_Z12.csv"
    out_debug = "2_W12_debug.csv"

    # 讀取資料
    df_x = pd.read_csv(x_file)
    df_y = pd.read_csv(y_file)

    # 建立 Y 的 mapping：Molecular_Formula → set of Trimmed_SMILES
    y_map = defaultdict(set)
    for _, row in df_y.iterrows():
        mf = row["Molecular_Formula"]
        ts = row["Trimmed_SMILES"]
        if pd.notna(mf) and pd.notna(ts):
            y_map[mf].add(ts)

    matched_rows = []
    unmatched_rows = []
    debug_rows = []

    for _, row in df_x.iterrows():
        modified_formula = row["Modified_Formula"]
        x_smile = row["SMILES"]

        if pd.isna(modified_formula) or pd.isna(x_smile):
            continue

        x_filtered = filter_smile_CO_only(x_smile)
        y_trimmed_set = y_map.get(modified_formula, set())
        matched_y_value = None

        # 執行比對
        for y_trimmed in y_trimmed_set:
            if is_match_by_removing_one_O_from_X(x_filtered, y_trimmed):
                matched_y_value = y_trimmed
                break

        # 複製資料並加入 debug 欄位
        new_row = row.copy()
        new_row["Filtered_SMILES_X"] = x_filtered
        new_row["Y_Trimmed_Candidates"] = ";".join(y_trimmed_set)
        new_row["Matched_Y_Trimmed"] = matched_y_value if matched_y_value else ""
        new_row["Match_Found"] = bool(matched_y_value)

        debug_rows.append(new_row)

        if matched_y_value:
            matched_rows.append(new_row)
        else:
            unmatched_rows.append(new_row)

    # 輸出結果
    pd.DataFrame(matched_rows).to_csv(out_match, index=False)
    pd.DataFrame(unmatched_rows).to_csv(out_unmatch, index=False)
    pd.DataFrame(debug_rows).to_csv(out_debug, index=False)

    print("✅ 比對完成")
    print(f"✔️ 有匹配：{len(matched_rows)} 筆 → {out_match}")
    print(f"❌ 無匹配：{len(unmatched_rows)} 筆 → {out_unmatch}")
    print(f"🧪 Debug 輸出：{len(debug_rows)} 筆 → {out_debug}")

if __name__ == "__main__":
    main()