import re
from collections import Counter

ELEMENT_ORDER = ["C", "H", "O"]   # 重組時的優先順序，可自行擴充/調整

# --- 1) 解析 "C6H12O6" -> {"C":6,"H":12,"O":6} ---
def parse_formula(formula: str) -> Counter:
    tokens = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    return Counter({el: int(num) if num else 1 for el, num in tokens})

# --- 2) 將 dict -> 分子式字串 ---
def compose_formula(elem_cnt: Counter) -> str:
    parts = []
    # 先照預設順序，再加其餘元素
    for el in ELEMENT_ORDER + [e for e in elem_cnt if e not in ELEMENT_ORDER]:
        cnt = elem_cnt.get(el, 0)
        if cnt > 0:
            parts.append(f"{el}{cnt if cnt>1 else ''}")
    return "".join(parts)

# --- 3) 解析指令 "+2H,-O,+C" -> {"H":+2, "O":-1, "C":+1} ---
def parse_delta(cmd: str) -> Counter:
    if not cmd.strip():
        return Counter()           # 空字串 → 不調整
    delta = Counter()
    for piece in cmd.split(","):
        piece = piece.strip()
        m = re.fullmatch(r"([+-])(\d*)([A-Z][a-z]?)", piece)
        if not m:
            raise ValueError(f"無效指令片段：{piece}")
        sign, num, el = m.groups()
        k = int(num) if num else 1
        delta[el] += k if sign == "+" else -k
    return delta

# --- 4) 依 delta 調整分子式 ---
def adjust_formula(formula: str, delta: Counter) -> str:
    cnt = parse_formula(formula) + delta
    # 不可有負數
    for el, v in cnt.items():
        if v < 0:
            raise ValueError(f"{formula} 調整後 {el} 變成負數")
    # 去掉 0
    cnt += Counter()  # 刪 key<=0
    return compose_formula(cnt)
