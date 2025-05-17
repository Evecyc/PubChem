import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout
)

from test_calculater import calculate  # 匯入你原本寫的功能

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧮 簡易計算機")
        self.setGeometry(100, 100, 400, 150)
        self.initUI()

    def initUI(self):
        self.input_label = QLabel("請輸入算式（例如：3 + 4 * 2）：", self)
        self.input_field = QLineEdit(self)

        self.result_label = QLabel("➡️ 結果會顯示在這裡", self)

        self.calc_button = QPushButton("計算", self)
        self.calc_button.clicked.connect(self.handle_calculate)

        # 排版
        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def handle_calculate(self):
        expr = self.input_field.text()
        result = calculate(expr)
        self.result_label.setText(f"➡️ 結果：{result}")

# 啟動程式
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())
