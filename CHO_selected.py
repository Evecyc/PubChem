import pandas as pd
import re

# --- 分子式過濾函式：只保留 C、H、O ---
def is_CHO_only(formula):
    if pd.isna(formula):
        return False

    # 若含有非法字元（如 + - . 空白 括號 等）直接過濾掉
    if re.search(r'[^CHO0-9]', formula):
        return False

    # 繼續解析元素，確保只出現 C/H/O
    elements = re.findall(r'([A-Z][a-z]?)', formula)
    return all(elem in {"C", "H", "O"} for elem in elements)

# --- 主程式 ---
def main():
    input_file = "3-hydroxy-4-methoxyphenyl.csv"
    output_file = "3-hydroxy-4-methoxyphenyl_CHO.csv"

    print(f"📥 讀取檔案：{input_file}")
    df = pd.read_csv(input_file)

    print(f"🔍 篩選只包含 C/H/O 的分子式...")
    df_filtered = df[df["Molecular_Formula"].apply(is_CHO_only)]

    print(f"✅ 保留筆數：{len(df_filtered)} / {len(df)}")
    print(f"💾 輸出檔案：{output_file}")
    df_filtered.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
