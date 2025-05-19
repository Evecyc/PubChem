import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import traceback

from analyze_compounds import analyze_compounds

# --------------------------------------------------
# Global dataframe holders
# --------------------------------------------------
x_df = pd.DataFrame()
y_dfs = []

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
            x_status.config(text=f"✅ 已上傳 X 檔案：{file_path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("錯誤", f"讀取 X 檔案失敗：{e}")

def upload_y_files():
    global y_dfs
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if file_paths:
        if len(file_paths) > 5:
            messagebox.showerror("錯誤", "最多僅支援 5 個 Y 檔案")
            return
        try:
            y_dfs = [pd.read_csv(fp) for fp in file_paths]
            y_status.config(text=f"✅ 已上傳 {len(y_dfs)} 個 Y 檔案")
        except Exception as e:
            messagebox.showerror("錯誤", f"讀取 Y 檔案失敗：{e}")

# --------------------------------------------------
# GUI callback
# --------------------------------------------------
def run_analysis():
    global x_df, y_dfs
    if x_df.empty or not y_dfs:
        messagebox.showerror("錯誤", "請先上傳 X 與至少一個 Y 檔案")
        return

    for w in root.grid_slaves():
        if int(w.grid_info()["row"]) >= 4:
            w.destroy()

    status = tk.Label(root, text="⏳ 正在分析中…")
    status.grid(row=4, column=0, columnspan=2, sticky="w", padx=10)
    root.update()

    try:
        # normalize column names
        x_df.rename(columns={"Molecular_Formula": "MolecularFormula"}, inplace=True)
        for df in y_dfs:
            df.rename(columns={"Molecular_Formula": "MolecularFormula"}, inplace=True)

        generated = analyze_compounds(x_df, y_dfs)

        row = 4
        for key, df in generated.items():
            if df.empty:
                continue
            def save_csv(k=key, d=df):
                path = filedialog.asksaveasfilename(initialfile=f"{k}.csv", defaultextension=".csv", filetypes=[["CSV", "*.csv"]])
                if path:
                    d.to_csv(path, index=False)
            tk.Button(root, text=f"下載 {key}.csv", command=save_csv).grid(row=row, column=0, sticky="w", padx=10, pady=2)
            tk.Label(root, text=f"📘 {get_desc(key)}", fg="gray", justify="left", wraplength=600).grid(row=row, column=1, sticky="w", padx=10)
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

tk.Label(root, text="請上傳 X 檔案：").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Button(root, text="上傳 X 檔案", command=upload_x_file).grid(row=0, column=1, sticky="w", pady=5)
x_status = tk.Label(root, text="❌ 尚未上傳", fg="red")
x_status.grid(row=0, column=2, sticky="w")

tk.Label(root, text="請上傳 Y 檔案（最多 5 個）：").grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Button(root, text="上傳 Y 檔案", command=upload_y_files).grid(row=1, column=1, sticky="w", pady=5)
y_status = tk.Label(root, text="❌ 尚未上傳", fg="red")
y_status.grid(row=1, column=2, sticky="w")

tk.Button(root, text="執行分析並產生檔案", command=run_analysis).grid(row=2, column=0, columnspan=3, pady=15)

root.mainloop()
