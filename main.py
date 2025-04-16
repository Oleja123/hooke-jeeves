import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
import os
import sympy
from algo.hooke_jeeves import execute


MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 400


def get_center():
    screen_geometry = QDesktopWidget().screenGeometry()
    cx = (screen_geometry.width() // 2) - MAIN_WINDOW_WIDTH // 2
    cy = (screen_geometry.height() // 2) - MAIN_WINDOW_HEIGHT // 2
    return (cx, cy)


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    main_window.setWindowTitle('Алгоритм Хука - Дживса')
    main_window.setGeometry(
        *get_center(), MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
    main_window.setFixedSize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

    menubar = main_window.menuBar()

    file_menu = menubar.addMenu('Файл')
    select_file = QtWidgets.QAction('Открыть', file_menu)
    file_menu.addAction(select_file)

    label1 = QtWidgets.QLabel(main_window)
    label1.setText('переменные')
    label1.move(100, 75)
    label2 = QtWidgets.QLabel(main_window)
    label2.setText('функция')
    label2.move(100, 175)
    variables = QtWidgets.QLineEdit(main_window)
    funct = QtWidgets.QLineEdit(main_window)
    variables.setFixedWidth(400)
    funct.setFixedWidth(400)
    variables.move(100, 100)
    funct.move(100, 200)
    btn = QtWidgets.QPushButton(main_window)
    btn.setText('Решить')
    btn.move(MAIN_WINDOW_WIDTH // 2 - btn.width() // 2, 300)

    def solve():
        try:
            vars = sympy.symbols(variables.text())
            expr = sympy.sympify(funct.text())
            res = execute(vars, expr, 1e-3, 2, 1.01, [1e-1 for i in range(len(vars))], [-2 for i in range(len(vars))])

            rs = ''
            for name in res:
                rs += f"{name} = {res[name]}\n"

            QtWidgets.QMessageBox.information(None, "Ответ", rs)
        except Exception:
            error = QtWidgets.QMessageBox()
            error.setWindowTitle('Ошибка')
            error.setText('Проверьте данные')

            error.exec_()

    def select_file_f():
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Выберите файл",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if(file_path):
            file = open(file_path)
            lines = file.readlines()
            variables.setText(lines[0][:-1])
            funct.setText(lines[1][:-1])
            file.close()

    select_file.triggered.connect(select_file_f)
    btn.clicked.connect(solve)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
