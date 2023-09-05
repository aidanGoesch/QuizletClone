import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QScrollArea, QGridLayout, QPlainTextEdit, QPushButton
from PyQt6.QtGui import QAction, QFont, QKeyEvent, QTextCursor
from PyQt6.QtCore import Qt
from source.Backend.flashcard import FlashCard
from source.Backend.study_set import StudySet
from source.Backend.file_handler import Writer
from source.Backend.Log.logging import log
from source.Frontend.Flashcards.flashcard_main import FlashCardGUI


class FocusPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            self.parent().focusNextChild()
        else:
            super().keyPressEvent(event)



# Add an option to delete certain flash cards

class Editor(QMainWindow):
    def __init__(self, geometry = None, study_set: StudySet = StudySet("", [])):
        self.rows = 10
        if len(study_set.flashcards) > 0:
            self.rows = len(study_set.flashcards)

        super().__init__()

        self.title = study_set.title
        self.description = study_set.description
        self.flashcards = study_set.flashcards
        self.study_set = study_set

        self.initUI(geometry)

    def initUI(self, geometry): # add delete buttton
        self.setWindowTitle("Editor")

        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu("File")
        file_menu.setStyleSheet("color: white; background-color: rgb(73, 91, 85);")

        new_action = QAction("New", self)
        new_action.triggered.connect(lambda : self.make_new())

        save_action = QAction("Save", self)
        save_action.triggered.connect(lambda : self.write_data())

        close_action = QAction("Close", self)
        close_action.triggered.connect(lambda : self.open_study_set())

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(quit)

        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(close_action)
        file_menu.addAction(exit_action)

        study_menu = menubar.addMenu("Study")
        study_menu.setStyleSheet("color: white; background-color: rgb(73, 91, 85);")

        flashcard_action = QAction("Flashcards", self)
        flashcard_action.triggered.connect(lambda : self.open_flashcards())

        learn_action = QAction("Learn", self)
        learn_action.triggered.connect(lambda : self.open_learn())

        study_menu.addAction(flashcard_action)
        study_menu.addAction(learn_action)


        # Create a scrollable widget and set it as the central widget of the main window
        scroll_widget = QWidget()
        self.setCentralWidget(scroll_widget)

        # Create a layout for the scrollable widget
        self.layout = QGridLayout(scroll_widget)

        #Add spot for Title
        title = FocusPlainTextEdit()
        title.setMinimumHeight(70)
        title.setFont(QFont('Times', 20))

        if self.title != "":
            title.setPlainText(self.title)
        else:
            title.setPlaceholderText("Title")

        title.setStyleSheet("color: white; background-color: rgb(73, 91, 85); border-radius: 10px;")
        self.layout.addWidget(title, 0, 0, 1, 2)

        # Add spot for description
        desc = FocusPlainTextEdit()
        desc.setMinimumHeight(90)
        desc.setFont(QFont('Times', 17))
        desc.setStyleSheet("color: white; background-color: rgb(73, 91, 85); border-radius: 10px;")

        if self.description != "":
            desc.setPlainText(self.description)
        else:
            desc.setPlaceholderText("Description")

        self.layout.addWidget(desc, 1, 0, 1, 2)

        # Create text boxes
        is_loaded = len(self.flashcards) != 0
        columns = 2
        for row in range(3, self.rows + 3):
            for col in range(columns):
                index = row * columns + col
                text_box = FocusPlainTextEdit()
                text_box.setMinimumHeight(60)
                text_box.setStyleSheet("color: white; background-color: rgb(73, 91, 85); border-radius: 10px;")
                # text_box.setFont(QFont('Times', 12))

                if not is_loaded:
                    if col == 0:
                        text_box.setPlaceholderText("Term")
                    else:
                        text_box.setPlaceholderText("Definition")
                else:
                    if col == 0:
                        text_box.setPlainText(self.flashcards[row-3].term)
                    else:
                        text_box.setPlainText(self.flashcards[row - 3].definition)

                self.layout.addWidget(text_box, row, col)


        def add_row():
            for col in range(columns):
                text_box = FocusPlainTextEdit()
                text_box.setMinimumHeight(60)
                text_box.setStyleSheet("color: white; background-color: rgb(73, 91, 85); border-radius: 10px;")

                if col == 0:
                    text_box.setPlaceholderText("Term")
                else:
                    text_box.setPlaceholderText("Definition")

                self.layout.addWidget(text_box, self.rows + 3, col)

            self.rows += 1
            self.layout.addWidget(add_row_button, self.rows + 3, 0, 1, 2)


        add_row_button = QPushButton(text = "Add Row")
        add_row_button.setMinimumHeight(40)
        add_row_button.clicked.connect(add_row)
        add_row_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")
        self.layout.addWidget(add_row_button, self.rows + 3, 0, 1, 2)

        # Create a scroll area and set the scrollable widget as its content
        scroll_bar_style = """
            QScrollBar:vertical {
                background: rgb(28, 44, 37);
                width: 15px;
            }
        
            QScrollBar::handle:vertical {
                background: rgb(73, 91, 85);
                min-height: 20px;
                border-radius: 10px;
            }
        
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: rgb(28, 44, 37);
            }
        
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
            }
        """

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setStyleSheet(scroll_bar_style)

        self.setCentralWidget(scroll_area)

        self.setStyleSheet("background-color: rgb(28, 44, 37);")

        self.menuBar().setStyleSheet("QMenuBar { color: white; background-color: rgb(38, 69, 62);}"
                                     "QMenuBar::item:selected { background-color: rgb(73, 91, 85);}")

        if geometry is None:
            self.setGeometry(200, 200, 700, 500)
        else:
            self.setGeometry(geometry)

        self.show()

    def extract_data(self) -> StudySet:
        def get_text_from_layout(item):
            widget = item.widget()
            return widget.toPlainText()


        study_set = StudySet("", [])
        index = 0
        for r in range(self.layout.rowCount()):
            if r == 0:
                item = self.layout.itemAtPosition(r, 0)
                study_set.title = get_text_from_layout(item)
            elif r == 1:
                item = self.layout.itemAtPosition(r, 0)
                study_set.description = get_text_from_layout(item)
            else:
                term, definition = '', ''
                for c in range(2):
                    temp = self.layout.itemAtPosition(r, c)
                    if  temp is not None and isinstance(temp.widget(), QPlainTextEdit):
                        if c == 0:
                            term = get_text_from_layout(temp)
                        elif c == 1:
                            definition = get_text_from_layout(temp)
                if term != '':
                    study_set.flashcards.append(FlashCard(term, definition))
        return study_set

    def write_data(self):
        study_set = self.extract_data()
        if not study_set.is_empty():
            writer = Writer(study_set = study_set)
            writer.write_data_to_file()

            log(f'Study Set {study_set.title} Saved!')
        else:
            log('The Set is Empty')

    def return_to_main(self):
        from source.Frontend.Editor.load_menu import LoadMenu

        main_menu = LoadMenu(self.geometry())
        main_menu.show()
        self.close()

    def make_new(self):
        new_set = Editor(self.geometry())
        new_set.show()
        self.close()

    def open_study_set(self):
        from source.Frontend.Editor.load_menu import LoadMenu
        load_menu = LoadMenu(self.geometry())
        load_menu.show()
        self.close()

    def open_flashcards(self):
        self.write_data()
        study_set = self.extract_data()
        if len(study_set.flashcards) > 0:
            flashcard_gui = FlashCardGUI(self.geometry(), study_set)
            flashcard_gui.show()
            self.close()

    def open_learn(self):
        from source.Frontend.Learn.learn_main import LearnGUI
        self.write_data()
        study_set = self.extract_data()
        learn_gui = LearnGUI(self.geometry(), study_set)
        learn_gui.show()
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Editor()
    sys.exit(app.exec())