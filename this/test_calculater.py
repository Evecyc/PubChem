# calculator.py

def calculate(expression):
    try:
        # 用 eval 安全地計算表達式
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except ZeroDivisionError:
        return "❌ 錯誤：除以零"
    except Exception as e:
        return f"❌ 錯誤：無效的輸入 ({e})"

def main():
    print("📟 歡迎使用簡易計算機（輸入 'exit' 離開）")
    while True:
        expr = input("請輸入算式（例如：3 + 4 * 2）：")
        if expr.lower() == 'exit':
            print("👋 離開計算機")
            break
        result = calculate(expr)
        print(f"➡️ 結果：{result}")

if __name__ == "__main__":
    main()
