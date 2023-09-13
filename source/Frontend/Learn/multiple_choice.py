# File that holds the multiple choice option for learn mode
import sys
import random
from source.Backend.flashcard import FlashCard
from source.Backend.study_set import StudySet
from source.Backend.Log.logging import log
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QFont


# "background-color: lightgreen; color: blue" label style sheet example

class Option(QPushButton):
    def __init__(self, card: FlashCard, correct: bool = False):
        super().__init__(text=card.definition)
        self.card = card
        self.correct = correct


class MultipleChoice(QWidget):
    completed = pyqtSignal()
    problem = pyqtSignal()

    def __init__(self, flashcards: list[FlashCard], current_card: int = 0):
        super().__init__()
        self.flashcards = flashcards
        self.current_card = current_card
        self.permutations = min(len(flashcards), 8)
        self.initUI()

        # do this later
        # if 'yes' == self.flashcards[self.current_card].definition.lower():
        #     pass
        # elif 'no' == self.flashcards[self.current_card].definition.lower():
        #     pass
        # elif 'true' == self.flashcards[self.current_card].definition.lower():
        #     pass
        # elif 'false' == self.flashcards[self.current_card].definition.lower():
        #     pass
        # else:
        #     # code
        # Each option is 20 apart from eachother

    def initUI(self):
        self.layout = QGridLayout(self)

        self.term = QLabel(self.flashcards[self.current_card].term)
        self.term.setFont(QFont('Times', 20))
        self.term.setStyleSheet("color: white; border-radius: 10px;")
        self.term.setMinimumHeight(120)
        self.term.setMinimumWidth(350)
        self.term.setAlignment(Qt.AlignmentFlag.AlignCenter.AlignHCenter)

        self.layout.addWidget(self.term, 0, 0, 2, 2)

        def to_option(card: FlashCard):
            temp = Option(card)
            temp.setCheckable(True)
            temp.setMinimumHeight(60)
            temp.setMinimumWidth(175)
            temp.setFont(QFont('Times', 15))
            temp.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")
            temp.clicked.connect(self.check_selected)

            if temp.card == self.flashcards[self.current_card]:
                temp.correct = True

            return temp

        self.options = list(map(to_option, self.init_options()))

        if len(self.options) == 2:
            self.layout.addWidget(self.options[0], 2, 0, 2, 1)
            self.layout.addWidget(self.options[1], 2, 1, 2, 1)
        else:
            i = 0
            for x in range(2):
                for y in range(2):
                    try:
                        self.layout.addWidget(self.options[i], y + 2, x, 1, 1)
                        i += 1
                    except IndexError:
                        continue

        self.setStyleSheet("background-color: rgb(28, 44, 37);")
        self.show()


    def init_options(self):

        if len(self.flashcards) >= 4:
            temp = get_rand_cards(self.flashcards, self.flashcards[self.current_card], 3) \
                   + [self.flashcards[self.current_card]]
        elif len(self.flashcards) == 1:
            log("This set is only has 1 card")
            return self.flashcards
        elif len(self.flashcards) == 0:
            log("ERROR: there are no terms to study in this set")

        else:
            temp = get_rand_cards(self.flashcards, self.flashcards[self.current_card], len(self.flashcards) - 1) \
                   + [self.flashcards[self.current_card]]

        random.shuffle(temp)

        return temp


    def check_selected(self):
        def count_checked():
            num = 0
            for option in self.options:
                if option.isChecked():
                    num += 1
            return num

        self.checked_count = count_checked()

        if self.checked_count >= 1:
            for o in self.options:
                if not o.isChecked():
                    o.setCheckable(False)
                    if o.card != self.flashcards[self.current_card]:
                        o.setHidden(True)
                    elif o.card == self.flashcards[self.current_card]:
                        o.setStyleSheet("border :7px solid ; border-color : Green; border-radius: 10px; background-color: rgb(73, 91, 85); color: white")
                else:
                    if o.card == self.flashcards[self.current_card]:  # if correct answer
                        if o.card.familiarity == 0:
                            o.card.familiarity += 1

                        # Show an indicator of correctness
                        self.term.setText("<html><font size=4 color='green'>Correct!</font> <br> <font size=1 color='grey'>Hit Enter to go to the Next Question</font></html>")
                        self.term.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.term.setStyleSheet("border :7px solid ; border-color : Green; border-radius: 10px; color: white")

                        o.setStyleSheet("border :7px solid ; border-color : Green; color: white; background-color: rgb(73, 91, 85); border-radius: 10px;")

                        # Show next button
                        self.installEventFilter(self)
                    else:  # if incorrect answer
                        # Show an indicator of incorrectness
                        self.term.setText("<html><font size=4 font color='#d22b2b'>Incorrect</font> <br> <font size=1 color='grey'>Hit Enter to go to the Next Question</font></html>")
                        self.term.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.term.setStyleSheet("border :7px solid ; border-color : rgb(210, 43, 43); border-radius: 10px; color: white")

                        o.setStyleSheet("border :7px solid ; border-color : rgb(210, 43, 43); border-radius: 10px; background-color: rgb(73, 91, 85); color: white")

                        # Show next button
                        self.installEventFilter(self)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.next_question()
                return True
        return super().eventFilter(obj, event)


    def reset_with_different_card(self):
        if self.current_card >= len(self.flashcards) - 1:
            self.current_card = 0
        else:
            self.current_card += 1

        self.removeEventFilter(self)
        self.term.setText(self.flashcards[self.current_card].term)

        temp = get_rand_cards(self.flashcards, self.flashcards[self.current_card], min(3, len(self.flashcards) - 1)) \
                + [self.flashcards[self.current_card]]
        random.shuffle(temp)
        for i, option in enumerate(self.options):
            option.card = temp[i]
            option.correct = temp[i] == self.flashcards[self.current_card]
            option.setText(temp[i].definition)
            option.setCheckable(True)
            option.setHidden(False)
            option.setChecked(False)
            option.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")

        self.term.setStyleSheet("color: white; border-radius: 10px;")
        self.term.setAlignment(Qt.AlignmentFlag.AlignCenter.AlignHCenter)


    def next_question(self):
        # print('next')
        if self.permutations == 1:
            if self.check_familiar():
                # print('done')
                self.completed.emit()
                self.hide()  # do this when all 8 cards have been studied
            else:
                random.shuffle(self.flashcards)
                self.reset_with_different_card()
                self.permutations = min(len(self.flashcards), 8)

        else:
            self.reset_with_different_card()
            self.permutations -= 1


    def check_familiar(self):
        for card in self.flashcards:
            if card.familiarity == 0:
                return False
        return True


def get_rand_cards(cards: list[FlashCard], current_card: FlashCard, sample_size: int) -> list[FlashCard]:
    return_val = random.sample(cards, sample_size)
    while current_card in return_val:
        return_val = random.sample(cards, sample_size)

    return return_val


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("MCQ Test")
    window.setGeometry(100, 100, 700, 500)

    test = MultipleChoice([FlashCard("Apple", "Yes"),
                           FlashCard("Orange", "Another Fruit"),
                           FlashCard("Pineapple", "A Third Fruit"),
                           FlashCard("Strawberry", "Yet Another Fruit"),
                           FlashCard("StarFruit", "A Fourth Fruit")])

    window.show()
    sys.exit(app.exec())