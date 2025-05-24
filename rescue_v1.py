# import pandas as pd
# import re
# from collections import defaultdict

# x_cut = -10
# y_cut = -11

# # --- 只保留 C 和 O 元素的 SMILES ---
# def filter_smile_CO_only(smile):
#     return ''.join(re.findall(r'[CO]', str(smile)))

# # --- 比對 prefix：X 去尾、Y 去尾，左側比對是否一致 ---
# def compare_prefix_to_cut_point(x_filtered, y_filtered):
#     prefix_x = x_filtered[:x_cut] if len(x_filtered) > abs(x_cut) else ""
#     prefix_y = y_filtered[:y_cut] if len(y_filtered) > abs(y_cut) else ""
#     return prefix_x == prefix_y, prefix_x, prefix_y

# # --- 主程式 ---
# def main():
#     # ✅ 修改為你實際的檔名
#     x_file = "unmatchY1_matchY2.csv"     # X：有 Modified_Formula 和 SMILES
#     y_file = "1,2-diol_CHO.csv"          # Y：原始資料，含 Molecular_Formula 和 SMILES

#     out_match = "WW2_11,12.csv"
#     out_unmatch = "Z2_11,12.csv"
#     out_y_filtered = "Y2_filtered_with_11,12prefix.csv"

#     print("📥 載入資料中...")
#     df_x = pd.read_csv(x_file)
#     df_y = pd.read_csv(y_file)

#     # ✅ 處理 Y：建立 Filtered_SMILES_Y 與 Prefix_Y，並儲存
#     df_y["Filtered_SMILES_Y"] = df_y["SMILES"].apply(filter_smile_CO_only)
#     df_y["Prefix_Y"] = df_y["Filtered_SMILES_Y"].apply(lambda s: s[:y_cut] if len(s) > abs(y_cut) else "")
#     df_y.to_csv(out_y_filtered, index=False)
#     print(f"💾 已輸出 Y 過濾結果至：{out_y_filtered}")

#     # ✅ 建立 Y 的 dict：Molecular_Formula 對應多筆 Y 資料
#     y_map = defaultdict(list)
#     for _, row in df_y.iterrows():
#         mf = row["Molecular_Formula"]
#         if pd.notna(mf):
#             y_map[mf].append(row)

#     matched_rows = []
#     unmatched_rows = []

#     print("🔍 開始進行 SMILES prefix 比對（多對一）...")

#     for _, row in df_x.iterrows():
#         modified_formula = row["Modified_Formula"]
#         x_smile = row["SMILES"]

#         if pd.isna(modified_formula) or pd.isna(x_smile):
#             continue

#         x_filtered = filter_smile_CO_only(x_smile)
#         prefix_x = x_filtered[:x_cut] if len(x_filtered) > abs(x_cut) else ""

#         matched_cids = []

#         for y_row in y_map.get(modified_formula, []):
#             y_filtered = y_row["Filtered_SMILES_Y"]
#             prefix_y = y_filtered[:y_cut] if len(y_filtered) > abs(y_cut) else ""
#             if prefix_x == prefix_y:
#                 matched_cids.append(str(y_row["Compound_CID"]))

#         new_row = row.copy()
#         new_row["Filtered_SMILES_X"] = x_filtered
#         new_row["Prefix_X"] = prefix_x
#         new_row["Matched_Y_SMILES_Count"] = len(matched_cids)
#         new_row["Matched_Y_CIDs"] = ";".join(matched_cids)

#         if matched_cids:
#             matched_rows.append(new_row)
#         else:
#             unmatched_rows.append(new_row)

#     # ✅ 輸出比對結果
#     pd.DataFrame(matched_rows).to_csv(out_match, index=False)
#     pd.DataFrame(unmatched_rows).to_csv(out_unmatch, index=False)

#     print("✅ 完成！")
#     print(f"✔️ 匹配成功筆數：{len(matched_rows)} → {out_match}")
#     print(f"❌ 全部不符筆數：{len(unmatched_rows)} → {out_unmatch}")

# if __name__ == "__main__":
#     main()

import pandas as pd
import re
from collections import defaultdict

# 只保留 C 和 O
def filter_smile_CO_only(smile):
    return ''.join(re.findall(r'[CO]', str(smile)))

# 比對邏輯：Y 比 X 多一個 O，刪除 Y 的其中一個 O 看是否與 X 相同
def is_match_by_removing_one_O(x_filtered, y_filtered):
    if len(y_filtered) != len(x_filtered) + 1:
        return False
    for i, c in enumerate(y_filtered):
        if c == 'O':
            candidate = y_filtered[:i] + y_filtered[i+1:]
            if candidate == x_filtered:
                return True
    return False

def main():
    # 📥 輸入檔案（請確認檔名正確）
    x_file = "2_W1.csv"     # 含 Modified_Formula 與 SMILES
    y_file = "2_Y.csv"          # 含 Molecular_Formula 與 SMILES

    # 📤 輸出檔案
    out_match = "2_WW1.csv"
    out_unmatch = "2_Z1.csv"
    out_y_filtered = "Y12_filtered_with_CO.csv"

    # 讀取資料
    print("📥 讀取 X、Y 檔案...")
    df_x = pd.read_csv(x_file)
    df_y = pd.read_csv(y_file)

    # 處理 Y：過濾 C/O 並儲存
    df_y["Filtered_SMILES_Y"] = df_y["SMILES"].apply(filter_smile_CO_only)
    df_y.to_csv(out_y_filtered, index=False)
    print(f"💾 已輸出過濾後的 Y：{out_y_filtered}")

    # 建立 Y 的 mapping（分子式 → list of rows）
    y_map = defaultdict(list)
    for _, row in df_y.iterrows():
        mf = row["Molecular_Formula"]
        if pd.notna(mf):
            y_map[mf].append(row)

    matched_rows = []
    unmatched_rows = []

    print("🔍 開始比對 Modified_Formula → Molecular_Formula → SMILES...")

    for _, row in df_x.iterrows():
        modified_formula = row["Modified_Formula"]
        x_smile = row["SMILES"]

        if pd.isna(modified_formula) or pd.isna(x_smile):
            continue

        x_filtered = filter_smile_CO_only(x_smile)
        matched_cids = []

        for y_row in y_map.get(modified_formula, []):
            y_filtered = y_row["Filtered_SMILES_Y"]
            if is_match_by_removing_one_O(x_filtered, y_filtered):
                matched_cids.append(str(y_row["Compound_CID"]))

        # 建立輸出資料列
        new_row = row.copy()
        new_row["Filtered_SMILES_X"] = x_filtered
        new_row["Matched_Y_SMILES_Count"] = len(matched_cids)
        new_row["Matched_Y_CIDs"] = ";".join(matched_cids)

        if matched_cids:
            matched_rows.append(new_row)
        else:
            unmatched_rows.append(new_row)

    # 儲存結果
    pd.DataFrame(matched_rows).to_csv(out_match, index=False)
    pd.DataFrame(unmatched_rows).to_csv(out_unmatch, index=False)

    print("✅ 比對完成！")
    print(f"✔️ 匹配成功：{len(matched_rows)} 筆 → {out_match}")
    print(f"❌ 完全不符：{len(unmatched_rows)} 筆 → {out_unmatch}")

if __name__ == "__main__":
    main()