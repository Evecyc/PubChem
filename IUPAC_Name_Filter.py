import pandas as pd

# 檔案路徑
# Case 1: X
#input_file = "hydroxyphenyl.csv"
#output_file = "4-hydroxyphenyl.csv"
# Case 1: Y1 & Case 2: X
#input_file = "dihydroxyphenyl.csv"
#output_file = "3,4-dihydroxyphenyl.csv"
# Case 1: Y2
# input_file = "diol.csv"
# output_file = "1,2-diol.csv"
# Case 2: Y1
# input_file = "hydroxy_methoxyphenyl.csv"
# output_file = "4-hydroxy-3-methoxyphenyl.csv"
# Case 2: Y2
input_file = "hydroxy_methoxyphenyl.csv"
output_file = "3-hydroxy-4-methoxyphenyl.csv"

# 要保留的欄位
columns_to_keep = [
    "Compound_CID",
    "Molecular_Weight",
    "IUPAC_Name",
    "Molecular_Formula",
    "SMILES",
    "Linked_PubChem_Literature_Count",
    "Linked_PubChem_Patent_Count"
]

# 分批讀取並篩選
chunk_size = 100000
filtered_chunks = []

for chunk in pd.read_csv(input_file, usecols=columns_to_keep, chunksize=chunk_size):
    #filtered = chunk[chunk["IUPAC_Name"].str.contains(r"\(4-hydroxyphenyl\)", na=False)]
    #filtered = chunk[chunk["IUPAC_Name"].str.contains(r"\(3,4-dihydroxyphenyl\)", na=False)]
    #filtered = chunk[chunk["IUPAC_Name"].str.contains("1,2-diol", na=False)]
    #filtered = chunk[chunk["IUPAC_Name"].str.contains(r"\(4-hydroxy-3-methoxyphenyl\)", na=False)]
    filtered = chunk[chunk["IUPAC_Name"].str.contains(r"\(3-hydroxy-4-methoxyphenyl\)", na=False)]
    filtered_chunks.append(filtered)

# 合併並輸出
if filtered_chunks:
    result = pd.concat(filtered_chunks)
    result.to_csv(output_file, index=False)
    print(f"✅ 完成！共 {len(result)} 筆符合條件的資料已儲存為 {output_file}")
else:
    print("⚠️ 沒有找到符合的資料。")