import os
import sys
import csv
import random

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.Qt import QMainWindow, QApplication, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap, QFont

roulette = None

cells_count = int()
not_empty_cells_count = int()

def calculate_time(rating) -> str:
    return str(rating)

def last_letter(rating) -> str:
    last_letter = ''
    if str(rating)[-1] == '1':
        last_letter = 'а'
    if int(str(rating)[-1]) in range(2, 5):
        last_letter = 'ы'
    if 11 <= int(rating) <= 19:
        last_letter = ''
    return last_letter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.setFixedSize(self.size())
        self.const_upper_label.setFont(QFont("Gill Sans Nova", 44))
        self.const_upper_label.setStyleSheet('color: rgb(255, 255, 255);')
        self.const_lower_label.setFont(QFont("Gill Sans Nova", 32))
        self.const_lower_label.setStyleSheet('color: rgb(255, 255, 255);')
        self.const_upper_label.hide()
        self.const_lower_label.hide()
        self.rating = dict()
        self.questions = list()
        self.file_path = str()
        self.load_table()
        self.img_label.setPixmap(QPixmap('fresco.png'))
        self.time_label.setStyleSheet('color: rgb(255, 255, 255);')
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet('color: rgb(255, 255, 255);')
        self.set_question_button.clicked.connect(self.generate_secret)
        self.choose_file_button.clicked.connect(self.choose_file)
        self.refresh_questions_button.clicked.connect(self.import_questions_from_TeX)
        self.roulette_button.clicked.connect(self.show_roulette_dialog)
        self.cells_count_spin_box.valueChanged.connect(self.cells_count_spin_box_changed)

    def load_table(self):
        file_name = 'table.csv'
        os.system("wget --no-check-certificate --output-document=" + file_name + " 'https://docs.google.com/spreadsheet/ccc?key=1KmEtA7ARv2Giq68jhrRyx5V2YWAdmz2UM6Y-T8gLjUM&output=csv'")

        with open(file_name, encoding="utf8") as csv_file:
            names_col = str()
            temp_reader = csv.reader(csv_file)
            for row in temp_reader:
                names_col = row[0]
                break

        csv_file.close()

        with open(file_name, encoding="utf8") as csv_file:
            reader = csv.DictReader(csv_file)
            for element in reader:
                if element['Промежуточный рейтинг'] == '':
                    continue
                self.rating[element[names_col].strip()] = int(element['Промежуточный рейтинг'])
                self.name_combo_box.addItem(element[names_col].strip())

        csv_file.close()
        os.system('rm ' + file_name)

    def set_time_label(self):
        current_rating = self.rating[self.name_combo_box.currentText()]
        self.time_label.setText(calculate_time(current_rating) + " секунд" + last_letter(current_rating))

    def set_question_label(self):
        if len(self.questions) == 0:
            self.question_label.setText("Ещё вопросы?")
            return

        self.question_label.setText(str(self.questions.pop()))
        self.questions_count_label.setText("Осталось вопросов: " + str(len(self.questions)))

    def generate_secret(self):
        if self.name_combo_box.currentText() != 'Студент':
            self.const_upper_label.show()
            self.const_lower_label.show()
            self.set_time_label()
            self.set_question_label()

    def choose_file(self):
        self.file_path = QFileDialog.getOpenFileName(self, "Выбрать файл  с вопросами", ".", "TeX(*.tex);;")
        self.file_path = str(self.file_path[0])
        self.import_questions_from_TeX()

    def import_questions_from_TeX(self):
        self.questions = list()
        if self.file_path == '':
            return

        questions_file = open(self.file_path, "r")
        for line in questions_file:
            self.questions.append(line.split('%')[0].replace('$', '').strip() + '\n')

        random.shuffle(self.questions)
        questions_file.close()
        self.questions_count_label.setText("Осталось вопросов: " + str(len(self.questions)))

    def cells_count_spin_box_changed(self):
        self.not_empty_cells_count_spin_box.setMaximum(self.cells_count_spin_box.value())

    def show_roulette_dialog(self):
        global not_empty_cells_count, cells_count, roulette
        cells_count = self.cells_count_spin_box.value()
        not_empty_cells_count = self.not_empty_cells_count_spin_box.value()

        roulette = RouletteDialog()
        roulette.show()


class RouletteDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/roulette.ui', self)
        self.button_size = 130
        self.button_margin = 20
        self.selected_cell = 0
        self.not_empty_cells = set()
        self.roulette_buttons = list()

        max_x = 0
        max_y = 0

        global cells_count
        for i in range(cells_count):
            coords = [
                self.button_margin * (1 + i % 3) + self.button_size * (i % 3),
                self.button_margin * (1 + i // 3) + self.button_size * (i // 3),
            ]

            roulette_button = QtWidgets.QPushButton(self)
            roulette_button.setMinimumSize(QtCore.QSize(self.button_size, self.button_size))
            roulette_button.setGeometry(QtCore.QRect(coords[0], coords[1], self.button_size, self.button_size))
            roulette_button.setObjectName(str(i))
            roulette_button.setText("")

            roulette_button.clicked.connect(self.i_hate_python(i))
            
            self.roulette_buttons.append(roulette_button)

            max_x = max(max_x, self.button_margin * (1 + i % 3) + self.button_size * (1 + i % 3) + self.button_margin)
            max_y = max(max_y, self.button_margin * (1 + i // 3) + self.button_size * (1 + i // 3) + self.button_margin)
            
        self.setFixedSize(max_x, max_y)

    def shoot(self, button_number):
        global not_empty_cells_count, cells_count
        while len(self.not_empty_cells) < not_empty_cells_count:
            self.not_empty_cells.add(random.randint(0, cells_count - 1))

        for button in self.roulette_buttons:
            button.setEnabled(False)
            button.show()

        for cell in self.not_empty_cells:
            self.roulette_buttons[cell].setStyleSheet('background: rgb(0, 255, 0);')
            self.roulette_buttons[button_number].setStyleSheet('background: rgb(0, 150, 0);')

        if button_number not in self.not_empty_cells:
            self.roulette_buttons[button_number].setStyleSheet('background: rgb(150, 0, 0);')

    def i_hate_python(self, i):
        return lambda: self.shoot(i)


random.seed()

app = QApplication(sys.argv)
app.setFont(QFont("Gill Sans Nova", 11))

main = MainWindow()
main.show()

sys.exit(app.exec_())
