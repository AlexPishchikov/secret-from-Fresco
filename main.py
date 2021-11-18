import sys
from pathlib import Path

import csv
import re

from PyQt5.Qt import QMainWindow, QDialog, QApplication
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import QLineEdit, QTableWidgetItem, QDialog, QDialogButtonBox, QDesktopWidget
from PyQt5.QtGui import QKeyEvent, QPixmap, QFont, QFontDatabase


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.plus = []
        self.load_table('[Рейтинг] 1 семестр 2021 - Диф. Уравнения.csv')
        pixmap = QPixmap('fresco.png')
        self.img_label.setPixmap(pixmap)
        self.time_label.setStyleSheet('color: rgb(255, 255, 255);')
        self.button.clicked.connect(lambda: self.set_time_label())
        self.button.setAutoDefault(True)
        self.name.returnPressed.connect(self.button.click)

    def load_table(self, name):
        with open(name, encoding="utf8") as csvfile:
            first_col = str()
            temp_reader = csv.reader(csvfile)
            for row in temp_reader:
                first_col = row[0]
                break
        csvfile.close()

        with open(name, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for element in reader:
                student_name = element[first_col].strip()
                emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"
                    u"\U0001F300-\U0001F5FF"
                    u"\U0001F680-\U0001F6FF"
                    u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)
                student_name = emoji_pattern.sub(r'', student_name)
                self.plus.append([student_name.strip().upper(), element['Промежуточный рейтинг']])
        csvfile.close()

    def set_time_label(self):
        for i in range(len(self.plus)):
            if self.plus[i][0] == self.name.text().upper():
                self.time_label.setText(self.plus[i][1])
                break
            self.time_label.setText('-1')


app = QApplication(sys.argv)
main = MainWindow()
main.show()

sys.exit(app.exec_())
