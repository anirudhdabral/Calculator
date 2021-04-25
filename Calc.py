import keyboard
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import gui.imgcalc


class Calculator(QFrame):
    def __init__(self):
        super().__init__()
        loadUi('gui\calc.ui', self)
        self.setFixedSize(400, 572)
        self.previous_result = 0
        self.previous_expression = ''
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.operators = ['+', '-', '*', '/', '%', '**']
        self.lineEdit.setReadOnly(True)
        self.btnClear.clicked.connect(self.clear)
        self.btn1.clicked.connect(lambda: self.lineEdit.insert("1"))
        self.btn2.clicked.connect(lambda: self.lineEdit.insert("2"))
        self.btn3.clicked.connect(lambda: self.lineEdit.insert("3"))
        self.btn4.clicked.connect(lambda: self.lineEdit.insert("4"))
        self.btn5.clicked.connect(lambda: self.lineEdit.insert("5"))
        self.btn6.clicked.connect(lambda: self.lineEdit.insert("6"))
        self.btn7.clicked.connect(lambda: self.lineEdit.insert("7"))
        self.btn8.clicked.connect(lambda: self.lineEdit.insert("8"))
        self.btn9.clicked.connect(lambda: self.lineEdit.insert("9"))
        self.btn0.clicked.connect(lambda: self.lineEdit.insert("0"))
        self.btnBackspace.clicked.connect(lambda: self.lineEdit.backspace())
        self.btnPoint.clicked.connect(self.point)
        self.btnPlus.clicked.connect(self.add)
        self.btnMinus.clicked.connect(self.sub)
        self.btnMul.clicked.connect(self.mul)
        self.btnDiv.clicked.connect(self.div)
        self.btnModulus.clicked.connect(self.modulus)
        self.btnPower.clicked.connect(self.power)
        self.btnEval.clicked.connect(self.evaluate)
        keyboard.add_hotkey('1', lambda: self.lineEdit.insert('1'))
        keyboard.add_hotkey('2', lambda: self.lineEdit.insert('2'))
        keyboard.add_hotkey('3', lambda: self.lineEdit.insert('3'))
        keyboard.add_hotkey('4', lambda: self.lineEdit.insert('4'))
        keyboard.add_hotkey('5', lambda: self.lineEdit.insert('5'))
        keyboard.add_hotkey('6', lambda: self.lineEdit.insert('6'))
        keyboard.add_hotkey('7', lambda: self.lineEdit.insert('7'))
        keyboard.add_hotkey('8', lambda: self.lineEdit.insert('8'))
        keyboard.add_hotkey('9', lambda: self.lineEdit.insert('9'))
        keyboard.add_hotkey('0', lambda: self.lineEdit.insert('0'))
        keyboard.add_hotkey('backspace', lambda: self.lineEdit.backspace())
        keyboard.add_hotkey('+', self.add)
        keyboard.add_hotkey('-', self.sub)
        keyboard.add_hotkey('*', self.mul)
        keyboard.add_hotkey('/', self.div)

    def clear(self):
        self.lineEdit.clear()
        self.txtResult.clear()
        self.previous_result = 0
        self.previous_expression = ''

    def evaluate(self):
        expression = self.lineEdit.text()
        if expression == '':
            return
        elif expression[-1] in self.numbers:
            result = expression
        elif expression[-1] == '.':
            self.lineEdit.insert('0')
            result = self.lineEdit.text()
        elif expression[-1] in self.operators:
            last_num = ''
            for i in range(2, len(self.lineEdit.text()) + 1):
                if self.lineEdit.text()[-i] in self.operators:
                    break
                else:
                    last_num += self.lineEdit.text()[-i]
            self.lineEdit.insert(last_num)
            result = self.lineEdit.text()
        try:
            result = eval(result)
        except ZeroDivisionError:
            self.lineEdit.clear()
            self.txtResult.clear()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Alert!')
            msg.setText("Can't divide by 0")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        except SyntaxError or TypeError:
            self.txtResult.clear()
            self.lineEdit.clear()
            return
        if self.previous_result == result and self.previous_expression == expression:
            last_num = ''
            for i in range(1, len(self.lineEdit.text()) + 1):
                if self.lineEdit.text()[-i] in self.operators:
                    if self.lineEdit.text()[-(i + 1)] in self.operators:
                        last_operator = "**"
                    else:
                        last_operator = self.lineEdit.text()[-i]
                    self.lineEdit.clear()
                    self.lineEdit.insert(str(self.previous_result) + last_operator + last_num[::-1])
                    break
                else:
                    last_num += self.lineEdit.text()[-i]
            try:
                result = eval(self.lineEdit.text())
            except ZeroDivisionError:
                self.lineEdit.clear()
                self.txtResult.clear()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Alert!')
                msg.setText("Can't divide by 0")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            except SyntaxError or TypeError:
                self.txtResult.clear()
                self.lineEdit.clear()
                return
        self.previous_result = result
        self.previous_expression = self.lineEdit.text()
        self.txtResult.setText(str(result))

    def check(self):
        if self.lineEdit.text()[-1] in self.numbers:
            return False
        else:
            return True

    def point(self):
        try:
            last_input = self.lineEdit.text()[-1]
        except IndexError:
            return
        if last_input in self.operators:
            self.lineEdit.insert("0.")
            return
        last_num = []
        for i in range(1, len(self.lineEdit.text())):
            if self.lineEdit.text()[-i] in self.operators:
                break
            else:
                last_num.append(self.lineEdit.text()[-i])
        if '.' not in last_num:
            self.lineEdit.insert(".")

    def add(self):
        try:
            self.lineEdit.text()[-1]
        except IndexError:
            return
        if self.check():
            self.lineEdit.backspace()
        self.lineEdit.insert("+")

    def sub(self):
        try:
            self.lineEdit.text()[-1]
        except IndexError:
            return
        if self.check():
            self.lineEdit.backspace()
        self.lineEdit.insert("-")

    def mul(self):
        try:
            self.lineEdit.text()[-1]
        except IndexError:
            return
        if self.check():
            self.lineEdit.backspace()
        self.lineEdit.insert("*")

    def div(self):
        try:
            self.lineEdit.text()[-1]
        except IndexError:
            return
        if self.check():
            self.lineEdit.backspace()
        self.lineEdit.insert("/")

    def modulus(self):
        try:
            self.lineEdit.text()[-1]
        except IndexError:
            return
        if self.check():
            self.lineEdit.backspace()
        self.lineEdit.insert("%")

    def power(self):
        try:
            self.lineEdit.text()[-1]
        except IndexError:
            return
        if self.check():
            self.lineEdit.backspace()
        self.lineEdit.insert("**")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    app.exec_()
