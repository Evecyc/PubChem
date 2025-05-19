import pandas as pd
import re


# --------------------------------------------------
# 是否為只含 C/H/O 的分子式
# --------------------------------------------------
def is_CHO_only(formula: str) -> bool:
    if pd.isna(formula):
        return False
    # 含有其他原子或符號直接剔除
    if re.search(r'[^CHO0-9]', formula):
        return False
    # 確認元素只出現 C、H、O
    elements = re.findall(r'([A-Z][a-z]?)', formula)
    return all(elem in {"C", "H", "O"} for elem in elements)

# --------------------------------------------------
# 在分子式中「加一個氧」的處理
# --------------------------------------------------
def add_oxygen(formula: str) -> str:
    """
    e.g.  C6H6  -> C6H6O1
          C6H12O  -> C6H12O1
          C6H12O2 -> C6H12O3
    """
    o_pos = formula.find("O")
    if o_pos == -1:                       # 原本沒有 O
        return formula + "O1"
    tail = formula[o_pos + 1 :]
    m = re.match(r"(\d+)", tail)
    if m:                                 # O 後面本來就有數字
        new_num = int(m.group(1)) + 1
        return formula[:o_pos] + f"O{new_num}" + tail[m.end() :]
    else:                                 # O 後面沒數字
        return formula[: o_pos + 1] + "1" + tail

# --------------------------------------------------
# 主函式：供 gui.py 呼叫
# --------------------------------------------------
#def analyze_compounds(x_df: pd.DataFrame, y_dfs: list[pd.DataFrame]) -> dict[str, pd.DataFrame]:
def analyze_compounds(
    x_df: pd.DataFrame,
    y_dfs: list[pd.DataFrame],
    x_fragment: str | None = None,           # X 片段
    y_fragments: list[str | None] | None = None   # 每個 Y 的片段
) -> dict[str, pd.DataFrame]:


    """
    參數
    ----
    fragment : str，可選。若填寫，僅保留 IUPAC_Name 含此片段的 X 資料再做比對
    x_df   : DataFrame，必含 'MolecularFormula'
    y_dfs  : list of DataFrame，長度 1~5，每個也必含 'MolecularFormula' 與 'Compound_CID'

    回傳
    ----
    dict  { 類別字串 : DataFrame }，類別字串為：
           • Z0          → 全部 Y 都不匹配
           • match_all   → 跟所有 Y 都匹配
           • W123…       → 部分匹配（數字為 1-based 的 Y 編號）
    """
    if not 1 <= len(y_dfs) <= 5:
        raise ValueError("Y 檔案數量必須在 1～5 之間")


    # -------- 0. 依片段過濾 X --------
    if x_fragment:
        if "IUPAC_Name" not in x_df.columns:
            raise KeyError("X 缺少 IUPAC_Name 欄位")
        x_df = x_df[x_df["IUPAC_Name"].str.contains(x_fragment, case=False, na=False)]
        if x_df.empty:
            raise ValueError(f"X 無符合片段「{x_fragment}」的化合物")

    # -------- 0b. 依片段過濾每個 Y --------
    if y_fragments is None:
        y_fragments = [None] * len(y_dfs)
    if len(y_fragments) != len(y_dfs):
        raise ValueError("y_fragments 長度需與 y_dfs 相同")

    new_y_dfs = []
    for idx, (y, frag) in enumerate(zip(y_dfs, y_fragments), start=1):
        if frag:
            if "IUPAC_Name" not in y.columns:
                raise KeyError(f"Y{idx} 缺少 IUPAC_Name 欄位")
            y = y[y["IUPAC_Name"].str.contains(frag, case=False, na=False)]
            if y.empty:
                print(f"⚠️  Y{idx} 無符合片段「{frag}」，將以空表比對")
        new_y_dfs.append(y)
    y_dfs = new_y_dfs

    # -------- 1. 準備 X --------
    
    x = x_df.copy()
    x = x[x["MolecularFormula"].apply(is_CHO_only)].reset_index(drop=True)
    x["Modified_Formula"] = x["MolecularFormula"].apply(add_oxygen)

    # -------- 2. 為每個 Y 建立「分子式 → CID」對照表 --------
    match_cols = []      # 儲存各 Y 的 CID 映射結果
    for i, y in enumerate(y_dfs, start=1):
        y_clean = y[y["MolecularFormula"].apply(is_CHO_only)]
        y_map = dict(zip(y_clean["MolecularFormula"], y_clean["Compound_CID"]))
        match_cols.append(x["Modified_Formula"].map(y_map).rename(f"Y{i}_CID"))

    matches = pd.concat(match_cols, axis=1)  # shape = (len(x), num_Y)

    # -------- 3. 產生分類 Category --------
    def categorize(row) -> str:
        hit_flags = row.notna().values        # True/False 陣列
        if hit_flags.all():
            return "match_all"
        if not hit_flags.any():
            return "Z0"
        # 局部命中 → W ＋ 命中的 Y 編號（1-based）
        idxs = [str(i + 1) for i, hit in enumerate(hit_flags) if hit]
        return "W" + "".join(idxs)

    x["Category"] = matches.apply(categorize, axis=1)

    # -------- 4. 回傳 dict --------
    result = {}
    full_table = pd.concat([x, matches], axis=1)
    for cat in sorted(full_table["Category"].unique()):
        result[cat] = full_table[full_table["Category"] == cat].copy()

    return result
