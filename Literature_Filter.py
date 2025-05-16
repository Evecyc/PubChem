import pandas as pd

# 載入主檔案
# df = pd.read_csv("4-hydroxyphenyl.csv")
# df = pd.read_csv("3,4-dihydroxyphenyl.csv")
df = pd.read_csv("1,2-diol.csv")

# 確保數值欄位不是字串
df["Linked_PubChem_Literature_Count"] = pd.to_numeric(df["Linked_PubChem_Literature_Count"], errors="coerce").fillna(0).astype(int)
df["Linked_PubChem_Patent_Count"] = pd.to_numeric(df["Linked_PubChem_Patent_Count"], errors="coerce").fillna(0).astype(int)

# 群組一：無專利也無文獻
group1 = df[
    (df["Linked_PubChem_Literature_Count"] == 0) &
    (df["Linked_PubChem_Patent_Count"] == 0)
]
# group1.to_csv("hydro_00.csv", index=False)
group1.to_csv("diol_00.csv", index=False)

# 群組二：有專利但沒文獻
group2 = df[
    (df["Linked_PubChem_Literature_Count"] == 0) &
    (df["Linked_PubChem_Patent_Count"] != 0)
]
# group2.to_csv("hydro_0x.csv", index=False)
group2.to_csv("diol_0x.csv", index=False)

# 群組三：有文獻
group3 = df[
    (df["Linked_PubChem_Literature_Count"] != 0)
]
# group3.to_csv("hydro_xx.csv", index=False)
group3.to_csv("diol_xx.csv", index=False)

# 輸出分組結果
print("✅ 分組完成！")
print(f"無專利也無文獻筆數：{len(group1)}")
print(f"有專利但沒文獻筆數：{len(group2)}")
print(f"有文獻筆數：{len(group3)}")