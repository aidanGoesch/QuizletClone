# file that holds the learn mode

# ADD AN OPTION TO SHOW THE TERM OR THE DEFINITION

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QScrollArea, QPushButton, QGridLayout, QLabel
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtCore import Qt

from source.Frontend.Learn.multiple_choice import MultipleChoice
from source.Frontend.Learn.fill_in_the_blank import FillInBlank
from source.Backend.study_set import StudySet
from source.Backend.flashcard import FlashCard


class LearnGUI(QMainWindow):
    def __init__(self, geometry, study_set: StudySet):
        super().__init__()
        self.study_set = study_set
        self.flash_cards = partition_flashcards(study_set.flashcards)
        self.current_block = 0

        self.initUI(geometry)


    def initUI(self, geometry):
        self.setWindowTitle("Learn")
        self.setGeometry(geometry)
        self.setStyleSheet("background-color: rgb(28, 44, 37);")

        menubar = self.menuBar()
        self.menuBar().setStyleSheet("QMenuBar { color: white; background-color: rgb(38, 69, 62);}"
                                     "QMenuBar::item:selected { background-color: rgb(73, 91, 85);}")

        # Create File menu
        file_menu = menubar.addMenu("File")
        file_menu.setStyleSheet("color: white; background-color: rgb(73, 91, 85);")

        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(lambda: self.return_to_editor())

        close_action = QAction("Close", self)
        close_action.triggered.connect(lambda: self.return_to_menu())

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(quit)


        file_menu.addAction(edit_action)
        file_menu.addAction(close_action)
        file_menu.addAction(exit_action)

        w = QWidget()
        self.setCentralWidget(w)

        self.layout = QGridLayout(w)

        self.questions = MultipleChoice(self.flash_cards[self.current_block], current_card=0)
        self.questions.completed.connect(lambda : self.switch_to_fill_in_blank())

        self.layout.addWidget(self.questions)  # need to pass in 8 cards

        self.show()


    def switch_to_fill_in_blank(self):
        self.questions = FillInBlank(self.flash_cards[self.current_block], current_card=0)
        self.questions.completed.connect(lambda : self.advance_study_block())

        self.layout.addWidget(self.questions)


    def advance_study_block(self):
        if self.current_block == len(self.flash_cards) - 1:
            self.finish_learn()
        else:
            self.current_block += 1
            self.questions = MultipleChoice(self.flash_cards[self.current_block], current_card=0)
            self.questions.completed.connect(lambda: self.switch_to_fill_in_blank())
            self.layout.addWidget(self.questions)


    def finish_learn(self):
        finished_screen = QLabel(
            "<html><font size=4 color='green'>Congratulations!</font> <br> <font size=1 color='grey'>You have learned all of the terms</font></html>")
        finished_screen.setFont(QFont('Times', 40))
        finished_screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        finished_screen.setStyleSheet("border :7px solid ; border-color : Green;")

        self.layout.addWidget(finished_screen)

        back_button = QPushButton("Return to Menu")
        back_button.setFont(QFont('Times', 20))
        back_button.setMinimumHeight(50)
        back_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")
        back_button.clicked.connect(lambda : self.return_to_menu())
        self.layout.addWidget(back_button)


    def return_to_menu(self):
        from source.Frontend.Editor.load_menu import LoadMenu
        main_window = LoadMenu()
        main_window.show()
        self.close()


    def return_to_editor(self):
        from source.Frontend.Editor.editor import Editor
        editor = Editor(self.geometry(), self.study_set)
        editor.show()
        self.close()


def partition_flashcards(flashcards: list[FlashCard]) -> list[list[FlashCard]]:
    temp_flashcards = flashcards[:]
    study_blocks = []
    if len(flashcards) < 8:
        study_blocks.append(flashcards)
        return study_blocks
    else:
        stop = 8
        if len(flashcards) % 8 == 0:
            for i in range(len(flashcards) // 8):
                study_blocks.append(flashcards[i * 8 : stop])
                stop += 8
            return study_blocks
        else:
            step = (len(flashcards) // 8) + 1

            for i in range(step):
                study_blocks.append([])

            while temp_flashcards != []:
                for j in range(step):
                    try:
                        study_blocks[j].append(temp_flashcards[-1])
                        temp_flashcards.remove(temp_flashcards[-1])
                    except IndexError:
                        return study_blocks
            return study_blocks


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LearnGUI(StudySet("", [FlashCard("Apple", "Yes"),
                           FlashCard("Orange", "Another Fruit"),
                           FlashCard("Pineapple", "A Third Fruit"),
                           FlashCard("Strawberry", "Yet Another Fruit")]))
    sys.exit(app.exec())

