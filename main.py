import os
import sys
import csv
import random

from PyQt5 import uic
from PyQt5.Qt import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap

def calculate_time(rating) -> str:
    return str(rating)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
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
        self.time_label.setText(calculate_time(self.rating[self.name_combo_box.currentText()]))

    def set_question_label(self):
        if len(self.questions) == 0:
            self.question_label.setText("Ещё вопросы?")
            return
        self.question_label.setText(str(self.questions.pop()))
        self.questions_count_label.setText("Осталось вопросов: " + str(len(self.questions)))

    def generate_secret(self):
        if self.name_combo_box.currentText() != 'Студент':
            self.set_time_label()
            self.set_question_label()

    def choose_file(self):
        self.questions = list()
        self.file_path = QFileDialog.getOpenFileName(self, "Выбрать файл  с вопросами", ".", "TeX(*.tex);;")
        self.file_path = str(self.file_path[0])
        self.import_questions_from_TeX()
        self.questions_count_label.setText("Осталось вопросов: " + str(len(self.questions)))
    
    def import_questions_from_TeX(self):
        questions_file = open(self.file_path, "r")
        for line in questions_file:
            self.questions.append(line.split('%')[0].replace('$', '').strip() + '\n')
        random.shuffle(self.questions)
        questions_file.close()


random.seed()
app = QApplication(sys.argv)
main = MainWindow()
main.show()

sys.exit(app.exec_())
