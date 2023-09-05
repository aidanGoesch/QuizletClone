# File that holds the flashcard GUI class that will display flashcards on the screen
import sys

from source.Backend.flashcard import FlashCard
from source.Backend.study_set import StudySet
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout
from PyQt6.QtGui import QFont, QAction

class FlashCardGUI(QMainWindow):
    def __init__(self, geometry, study_set: StudySet):
        super().__init__()
        # width, height = window.width(), window.height()
        self.flashcards = study_set.flashcards
        self.study_set = study_set
        self.current_card = 0
        self.initUI(geometry)

    def initUI(self, geometry):
        self.setWindowTitle("Flashcards")
        self.setGeometry(geometry)
        self.setStyleSheet("background-color: rgb(28, 44, 37);")

        w = QWidget()
        self.setCentralWidget(w)
        layout = QGridLayout(w)

        menubar = self.menuBar()
        self.menuBar().setStyleSheet("QMenuBar { color: white; background-color: rgb(38, 69, 62);}"
                                     "QMenuBar::item:selected { background-color: rgb(73, 91, 85);}")

        # Create File menu
        file_menu = menubar.addMenu("File")
        file_menu.setStyleSheet("color: white; background-color: rgb(73, 91, 85);")

        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(lambda: self.open_editor())

        close_action = QAction("Close", self)
        close_action.triggered.connect(lambda: self.return_to_main())

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(quit)

        file_menu.addAction(edit_action)
        file_menu.addAction(close_action)
        file_menu.addAction(exit_action)

        # Flashcard Button
        self.card = QPushButton(text=self.flashcards[self.current_card].term)
        self.card.setCheckable(True)
        self.card.setMinimumHeight(350)
        self.card.setMinimumWidth(550)
        self.card.setFont(QFont('Times', 20))
        self.card.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")
        self.card.clicked.connect(self.flip)

        layout.addWidget(self.card, 0, 0, 1, 2)

        # Next Card Button
        self.next_button = QPushButton(text="Next")
        self.next_button.setCheckable(True)
        self.next_button.setMinimumHeight(100)
        self.next_button.setFont(QFont('Times', 13))
        self.next_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")
        self.next_button.clicked.connect(self.next_card)

        layout.addWidget(self.next_button, 1, 1, 1, 1)

        # Previous Card Button
        self.prev_button = QPushButton(text="Previous")
        self.prev_button.setCheckable(True)
        self.prev_button.setMinimumHeight(100)
        self.prev_button.setFont(QFont('Times', 13))
        self.prev_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")
        self.prev_button.clicked.connect(self.prev_card)

        layout.addWidget(self.prev_button, 1, 0, 1, 1)
        self.show()


    def flip(self):
        if self.card.isChecked():
            if self.card.text() == self.flashcards[self.current_card].term:
                self.card.setText(self.flashcards[self.current_card].definition)
            else:
                self.card.setText(self.flashcards[self.current_card].term)

            self.card.setChecked(False)

    def update_card(self):
        self.card.setText(self.flashcards[self.current_card].term)

    def next_card(self):
        # print('next')
        if self.current_card < len(self.flashcards) - 1:
            self.current_card += 1
            self.update_card()

        self.next_button.setChecked(False)

    def prev_card(self):
        # print('previous')
        if self.current_card > 0:
            self.current_card -= 1
            self.update_card()

        self.prev_button.setChecked(False)

    def return_to_main(self):
        from source.Frontend.Editor.load_menu import LoadMenu

        main_window = LoadMenu()
        main_window.show()
        self.close()

    def open_editor(self):
        from source.Frontend.Editor.editor import Editor

        self.editor_window = Editor(study_set = self.study_set)
        self.editor_window.show()
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FlashCardGUI([FlashCard("A Fruaa ahas as goang ao be a reaay a aaaaaaaa  aaaaaaaaaaaaaaaaaaaaaa  aaa aaaaaaaa aaaaaaaa aaaaaaaaaaa aaaaaaaaaaaaaaaa aaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaa aaa", "A Fruit this is going to be a realy long definition so that I can stress test the thing "), FlashCard("Orange", "Another Fruit")])
    sys.exit(app.exec())