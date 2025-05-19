import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import traceback

from analyze_compounds import analyze_compounds

# --------------------------------------------------
# Global holders
# --------------------------------------------------
x_df = pd.DataFrame()
y_dfs = []
y_fragment_entries = []   # 動態 Entry 物件

# --------------------------------------------------
# Helper: dynamic description
# --------------------------------------------------
def get_desc(key: str) -> str:
    if key == "Z0":
        return "加 O 後在所有 Y 中皆未匹配"
    if key == "match_all":
        return "加 O 後在所有 Y 中皆匹配"
    if key.startswith("W"):
        ys = ", ".join([f"Y{d}" for d in key[1:]])
        return f"加 O 後僅匹配 {ys}"
    return f"分類 {key}"

# --------------------------------------------------
# File upload callbacks
# --------------------------------------------------
def upload_x_file():
    global x_df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            x_df = pd.read_csv(file_path)
            x_df.rename(columns={"Molecular_Formula": "MolecularFormula"}, inplace=True)
            x_status.config(text=f"✅ 已上傳 X 檔案：{file_path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("錯誤", f"讀取 X 檔案失敗：{e}")

def upload_y_files():
    global y_dfs, y_fragment_entries
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if not file_paths:
        return
    if len(file_paths) > 5:
        messagebox.showerror("錯誤", "最多僅支援 5 個 Y 檔案")
        return
    try:
        # 讀取並標準化欄名
        y_dfs = []
        for fp in file_paths:
            df = pd.read_csv(fp)
            df.rename(columns={"Molecular_Formula": "MolecularFormula"}, inplace=True)
            y_dfs.append(df)
        y_status.config(text=f"✅ 已上傳 {len(y_dfs)} 個 Y 檔案")
    except Exception as e:
        messagebox.showerror("錯誤", f"讀取 Y 檔案失敗：{e}")
        return

    # 先清掉舊的 Y 片段輸入框
    for ent in y_fragment_entries:
        ent.destroy()
    y_fragment_entries.clear()

    # 動態新增 Y 片段輸入框
    base_row = 3   # row 0:X, 1:Y, 2:X片段
    for i in range(len(y_dfs)):
        tk.Label(root, text=f"Y{i+1} 片段（可留空）：").grid(row=base_row+i, column=0, sticky="e", padx=10, pady=2)
        ent = tk.Entry(root, width=25)
        ent.grid(row=base_row+i, column=1, sticky="w", pady=2)
        y_fragment_entries.append(ent)

    # 把「執行分析」按鈕往下推
    run_btn.grid(row=base_row+len(y_dfs), column=0, columnspan=3, pady=15)

# --------------------------------------------------
# GUI callback
# --------------------------------------------------
def run_analysis():
    global x_df, y_dfs
    if x_df.empty or not y_dfs:
        messagebox.showerror("錯誤", "請先上傳 X 與至少一個 Y 檔案")
        return

    # 清除先前結果區域 (row >= 10 保險起見)
    for w in root.grid_slaves():
        if int(w.grid_info()["row"]) >= 10:
            w.destroy()

    status = tk.Label(root, text="⏳ 正在分析中…")
    status.grid(row=10, column=0, columnspan=2, sticky="w", padx=10)
    root.update()

    try:
        # 取得片段設定
        x_fragment = x_fragment_entry.get().strip() or None
        y_fragments = [(e.get().strip() or None) for e in y_fragment_entries]

        # 執行分析
        generated = analyze_compounds(
            x_df, y_dfs,
            x_fragment=x_fragment,
            y_fragments=y_fragments
        )

        row = 11
        for key, df in generated.items():
            if df.empty:
                continue
            def save_csv(k=key, d=df):
                path = filedialog.asksaveasfilename(
                    initialfile=f"{k}.csv",
                    defaultextension=".csv",
                    filetypes=[("CSV", "*.csv")])
                if path:
                    d.to_csv(path, index=False)

            tk.Button(root, text=f"下載 {key}.csv", command=save_csv)\
                .grid(row=row, column=0, sticky="w", padx=10, pady=2)
            tk.Label(root, text=f"📘 {get_desc(key)}",
                     fg="gray", justify="left", wraplength=600)\
                .grid(row=row, column=1, sticky="w", padx=10)
            row += 1

        messagebox.showinfo("完成", "分析完成，可下載結果。")
    except Exception as exc:
        traceback.print_exc()
        messagebox.showerror("錯誤", f"處理失敗：{exc}")
    finally:
        status.destroy()

# --------------------------------------------------
# GUI layout
# --------------------------------------------------
root = tk.Tk()
root.title("PubChem 化學結構比對工具（上傳版）")

# X 上傳
tk.Label(root, text="請上傳 X 檔案：").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Button(root, text="上傳 X 檔案", command=upload_x_file)\
    .grid(row=0, column=1, sticky="w", pady=5)
x_status = tk.Label(root, text="❌ 尚未上傳", fg="red")
x_status.grid(row=0, column=2, sticky="w")

# Y 上傳
tk.Label(root, text="請上傳 Y 檔案（最多 5 個）：")\
    .grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Button(root, text="上傳 Y 檔案", command=upload_y_files)\
    .grid(row=1, column=1, sticky="w", pady=5)
y_status = tk.Label(root, text="❌ 尚未上傳", fg="red")
y_status.grid(row=1, column=2, sticky="w")

# X 片段輸入
tk.Label(root, text="X 片段（可留空）：")\
    .grid(row=2, column=0, sticky="e", padx=10, pady=5)
x_fragment_entry = tk.Entry(root, width=25)
x_fragment_entry.grid(row=2, column=1, sticky="w", pady=5)

# 執行按鈕 (row 3 會被動態調整)
run_btn = tk.Button(root, text="執行分析並產生檔案", command=run_analysis)
run_btn.grid(row=3, column=0, columnspan=3, pady=15)

root.mainloop()
