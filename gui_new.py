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
y_fragment_widgets = []   # Label + Entry → 只用來 destroy
y_fragment_entries = []   # 只存 Entry   → 供 run_analysis 讀 value
# --------------------------------------------------
# Helper: dynamic description
# --------------------------------------------------
def get_desc(key: str) -> str:
    if key == "Z0":
        return "unmatched in all Y"
    if key == "match_all":
        return "matched in all Y"
    if key.startswith("W"):
        ys = ", ".join([f"Y{d}" for d in key[1:]])
        return f"only matched in {ys}"
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
            x_status.config(text=f"✅ already uploaded：{file_path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("error", f"reading X files failed：{e}")

def upload_y_files():
    global y_dfs, y_fragment_entries
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if not file_paths:
        return
    if len(file_paths) > 5:
        messagebox.showerror("error", "only up to 5 Y files allowed")
        return
    try:
        # 讀取並標準化欄名
        y_dfs = []
        for fp in file_paths:
            df = pd.read_csv(fp)
            df.rename(columns={"Molecular_Formula": "MolecularFormula"}, inplace=True)
            y_dfs.append(df)
        y_status.config(text=f"✅ already uploaded {len(y_dfs)} Y files")
    except Exception as e:
        messagebox.showerror("error", f"reading Y files failed：{e}")
        return

    # --------------------------------------
    # 先清掉舊的 Y 片段 Label + Entry
    # --------------------------------------
    for w in y_fragment_entries:        # 這裡改名：存「所有元件」
        w.destroy()
    y_fragment_entries.clear()

    # --------------------------------------
    # 動態新增 Y 片段 Label/Entry
    # --------------------------------------
    base_row = 4          # 0:X  1:Y-upload  2:X片段  3:元素指令(初始放這)→實際會重排
    for i in range(len(y_dfs)):
        lbl = tk.Label(root, text=f"Y{i+1} segment (could be empty):")
        ent = tk.Entry(root, width=25)
        lbl.grid(row=base_row+i, column=0, sticky="e", padx=10, pady=2)
        ent = tk.Entry(root, width=25)
        ent.grid(row=base_row+i, column=1, sticky="w", pady=2)
        # 同時存 label 與 entry，方便下次一併 destroy
        y_fragment_widgets.extend([lbl, ent])
        y_fragment_entries.append(ent) 

    # --------------------------------------
    # 把「元素調整指令」Label/Entry 重新排到最下面
    # --------------------------------------
    delta_label.grid_forget()     # 先移除舊 grid (不刪 widget)
    delta_entry.grid_forget()

    row_after_Y = base_row + len(y_dfs)
    delta_label.grid(row=row_after_Y,   column=0, sticky="e", padx=10, pady=2)
    delta_entry.grid(row=row_after_Y,   column=1, sticky="w", pady=2)

    # --------------------------------------
    # 再把「執行分析」按鈕往下一列推
    # --------------------------------------
    run_btn.grid(row=row_after_Y + 1, column=0, columnspan=3, pady=15)


# --------------------------------------------------
# GUI callback
# --------------------------------------------------
def run_analysis():
    global x_df, y_dfs
    if x_df.empty or not y_dfs:
        messagebox.showerror("error", "please upload X and Y files first")
        return

    # 清除先前結果區域 (row >= 10 保險起見)
    for w in root.grid_slaves():
        if int(w.grid_info()["row"]) >= 10:
            w.destroy()

    status = tk.Label(root, text="⏳ running…")
    status.grid(row=10, column=0, columnspan=2, sticky="w", padx=10)
    root.update()

    try:
        # 取得片段設定
        x_fragment = x_fragment_entry.get().strip() or None
        y_fragments = [(e.get().strip() or None) for e in y_fragment_entries]

        delta_cmd = delta_entry.get().strip() or "+O" 

        generated = analyze_compounds(
        x_df, y_dfs,
        x_fragment=x_fragment,
        y_fragments=y_fragments,
        delta_cmd=delta_cmd
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

            tk.Button(root, text=f"download {key}.csv", command=save_csv)\
                .grid(row=row, column=0, sticky="w", padx=10, pady=2)
            tk.Label(root, text=f"📘 {get_desc(key)}",
                     fg="gray", justify="left", wraplength=600)\
                .grid(row=row, column=1, sticky="w", padx=10)
            row += 1

        messagebox.showinfo("completed", "analysis completed, download results.")
    except Exception as exc:
        traceback.print_exc()
        messagebox.showerror("error", f"failed:{exc}")
    finally:
        status.destroy()

# --------------------------------------------------
# GUI layout
# --------------------------------------------------
root = tk.Tk()
root.title("PDMA2 - Compound Analyzer")


# X 上傳
tk.Label(root, text="upload Ux file：").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Button(root, text="upload Ux file", command=upload_x_file)\
    .grid(row=0, column=1, sticky="w", pady=5)
x_status = tk.Label(root, text="❌ haven't uploaded", fg="red")
x_status.grid(row=0, column=2, sticky="w")

# Y 上傳
tk.Label(root, text="upload Uy files (up to 5)：")\
    .grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Button(root, text="upload Uy files", command=upload_y_files)\
    .grid(row=1, column=1, sticky="w", pady=5)
y_status = tk.Label(root, text="❌ haven't uploaded", fg="red")
y_status.grid(row=1, column=2, sticky="w")

# X 片段輸入
tk.Label(root, text="X segment (could be empty)：")\
    .grid(row=2, column=0, sticky="e", padx=10, pady=5)
x_fragment_entry = tk.Entry(root, width=25)
x_fragment_entry.grid(row=2, column=1, sticky="w", pady=5)


# 先建立元件，存成全域變數
delta_label = tk.Label(root, text="modification command (e.g., +O, +2H,-C)：")
delta_entry = tk.Entry(root, width=25)
delta_entry.insert(0, "+O")        # 預設值

# 一開始暫放在 row 3（之後 upload_y_files 會重新排位置）
delta_label.grid(row=3, column=0, sticky="e", padx=10, pady=2)
delta_entry.grid(row=3, column=1, sticky="w", pady=2)

# 執行按鈕 (row 3 會被動態調整)
run_btn = tk.Button(root, text="run analysis", command=run_analysis)
run_btn.grid(row=4, column=0, columnspan=3, pady=15)

root.mainloop()
