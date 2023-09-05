# File that stores the file in the blank widget for the learn mode
import sys
import random
from source.Backend.flashcard import FlashCard
from source.Backend.study_set import StudySet
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QPlainTextEdit
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QFont

class CheckTextEdit(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.enter_pressed = False

    def keyPressEvent(self, event):
        if event.type() == QEvent.Type.KeyPress and not self.enter_pressed:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.parentWidget().handleEnterKey()
            else:
                super().keyPressEvent(event)
        else:
            self.parentWidget().eventFilter(self, event)

class FillInBlank(QWidget):
    completed = pyqtSignal()
    def __init__(self, flashcards: list[FlashCard], current_card: int = 0):
        super().__init__()

        self.flashcards = flashcards
        self.current_card = current_card

        self.initUI()
        self.installEventFilter(self)

        self.enter_key_pressed = False


    def initUI(self):
        self.layout = QGridLayout(self)

        self.query = QLabel(self.flashcards[self.current_card].term)
        self.query.setFont(QFont('Times', 20))
        self.query.setStyleSheet("border: 1px solid black;")
        self.query.setMinimumHeight(120)
        self.query.setMinimumWidth(350)
        self.query.wordWrap()
        self.query.setStyleSheet("color: white; background-color: rgb(73, 91, 85); border-radius: 10px;")
        self.query.setAlignment(Qt.AlignmentFlag.AlignCenter.AlignHCenter)

        self.layout.addWidget(self.query, 0, 0, 2, 2)

        self.dialogue_box = CheckTextEdit()
        self.dialogue_box.setFont(QFont('Times', 15))
        self.dialogue_box.setMinimumHeight(60)
        self.dialogue_box.setMinimumWidth(350)
        self.dialogue_box.setStyleSheet("color: white; background-color: rgb(73, 91, 85); border-radius: 10px;")
        self.dialogue_box.setPlaceholderText("...")

        self.layout.addWidget(self.dialogue_box, 2, 0, 2, 1)

        self.override_button = QPushButton("override: I was right")
        self.override_button.setFont(QFont('Times', 10))
        self.override_button.setMinimumHeight(40)
        self.override_button.setMinimumWidth(350)
        self.override_button.setStyleSheet("QPushButton {color: white; background-color: transparent; border-radius: 10px;}"
                                           "QPushButton:hover {color: rgb(95, 185, 79); background-color: transparent; border-radius: 10px;}")
        self.override_button.setHidden(True)
        self.override_button.clicked.connect(lambda : self.override_question())

        self.layout.addWidget(self.override_button, 1, 0, 1, 1)

        self.setStyleSheet("background-color: rgb(28, 44, 37);")
        self.show()


    def handleEnterKey(self):
        self.enter_key_pressed = True
        self.dialogue_box.enter_pressed = True
        if self.dialogue_box.toPlainText().lower() == self.flashcards[self.current_card].definition.lower():
            self.flashcards.remove(self.flashcards[self.current_card])
            self.query.setText(
                "<html><font size=4 color='green'>Correct!</font> <br> <font size=1 color='grey'>Hit Any Key to go to the Next Question</font></html>")
            self.query.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.query.setStyleSheet("border :7px solid ; border-color : Green; border-radius: 10px;")

        else:
            self.query.setText(
                "<html><font size=4 font color='#d22b2b'>Incorrect</font> <br> <font size=1 color='grey'>Hit Any Key to go to the Next Question</font></html>")
            self.query.setAlignment(Qt.AlignmentFlag.AlignCenter.AlignHCenter)
            self.query.setStyleSheet("border :7px solid ; border-color : rgb(210, 43, 43); border-radius: 10px;")

            self.override_button.show()

    def override_question(self):
        self.flashcards.remove(self.flashcards[self.current_card])
        self.next_question()


    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if self.enter_key_pressed:
                self.next_question()
            return True
        else:
            return super().eventFilter(obj, event)


    def reset_with_new_card(self):
        self.current_card += 1

        self.removeEventFilter(self)
        self.enter_key_pressed = False
        self.dialogue_box.enter_pressed = False

        self.query.setText(self.flashcards[self.current_card].term)
        self.query.setStyleSheet("color: white; background-color: rgb(73, 91, 85); border-radius: 10px;")
        self.query.setAlignment(Qt.AlignmentFlag.AlignCenter.AlignHCenter)

        self.dialogue_box.setPlainText("")
        self.dialogue_box.setPlaceholderText("...")

        self.override_button.hide()


    def next_question(self):
        if self.current_card >= len(self.flashcards) - 1:
            if len(self.flashcards) == 0:
                self.completed.emit()
                self.hide()
            else:
                self.current_card = -1

        else:
            self.reset_with_new_card()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("MCQ Test")
    window.setGeometry(100, 100, 700, 500)

    test = FillInBlank([FlashCard("What does it look like when there just is a really long term so it has to wrap the text normally not just by spamming letters", "Yes"),
                           FlashCard("Orange", "Another Fruit"),
                           FlashCard("Pineapple", "A Third Fruit"),
                           FlashCard("Strawberry", "Yet Another Fruit")])

    window.show()
    sys.exit(app.exec())