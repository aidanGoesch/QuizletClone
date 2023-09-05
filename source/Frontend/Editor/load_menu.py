import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QScrollArea, QPushButton, QGridLayout, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from functools import partial
from source.Backend.flashcard import FlashCard
from source.Backend.study_set import StudySet
from source.Backend.file_handler import Loader
from source.Backend.Log.logging import log

class LoadMenu(QMainWindow):
    def __init__(self, geometry=None):
        super().__init__()

        self.loader = Loader()
        self.initUI(geometry)

    def initUI(self, geometry):  # 4 rows name is first 2 then study and edit
        self.setWindowTitle("Fake Quizlet")

        # Create a scrollable widget and set it as the central widget of the main window
        scroll_widget = QWidget()
        self.setCentralWidget(scroll_widget)

        # Create a layout for the scrollable widget
        self.layout = QGridLayout(scroll_widget)

        title = QLabel("Fake Quizlet")
        title.setMinimumHeight(200)
        title.setFont(QFont('Times', 50))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title, 0, 1, 1, 3)

        new_set_button = QPushButton("New Set")
        new_set_button.setMinimumHeight(90)
        new_set_button.setFont(QFont('Times', 15))
        new_set_button.clicked.connect(lambda : self.make_new_set())
        new_set_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                  "QPushButton:hover { border-color: white; }")

        self.layout.addWidget(new_set_button, 0, 5, 2, 2)


        file_names = self.loader.get_set_names()
        row = 1
        for name in file_names:
            file_header = QLabel("     " + name)
            file_header.setMinimumHeight(50)
            file_header.setFont(QFont('TImes', 10))
            file_header.setStyleSheet("color: white; background-color: rgb(50, 76, 59); border-radius: 10px;")

            self.layout.addWidget(file_header, row, 0, 1, 4)

            edit_button = QPushButton("Edit")
            edit_button.setMinimumHeight(50)
            edit_button.setFont(QFont('Times', 10))
            edit_button.clicked.connect(partial(self.open_editor, name))
            edit_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")

            self.layout.addWidget(edit_button, row, 4, 1, 3)

            delete_button = QPushButton("X")
            delete_button.setMinimumHeight(50)
            delete_button.setFont(QFont('Times', 10))
            delete_button.clicked.connect(partial(self.open_delete_dialogue, name))
            delete_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                      "color: rgb(210, 43, 43); background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                      "QPushButton:hover { border-color: white; }")

            self.layout.addWidget(delete_button, row, 8, 1, 1)

            row += 1


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

        if geometry is None:
            self.setGeometry(200, 200, 700, 500)
        else:
            self.setGeometry(geometry)
        self.setStyleSheet("background-color: rgb(28, 44, 37);")
        self.show()

    def open_editor(self, set_name: str):
        from source.Frontend.Editor.editor import Editor
        log(f"being editted: {set_name}")
        study_set = Loader().get_data_from_file(set_name)

        editor = Editor(geometry=self.geometry(), study_set=study_set)
        editor.show()
        self.close()

    def make_new_set(self):
        from source.Frontend.Editor.editor import Editor
        editor = Editor(self.geometry())
        editor.show()
        self.close()

    def open_delete_dialogue(self, file_name: str):
        from source.Frontend.Editor.delete_dialogue import DeleteDialogue
        dialogue = DeleteDialogue(self.geometry(), file_name)
        dialogue.deleted.connect(lambda : self.refresh_window())
        dialogue.show()

    def refresh_window(self):
        self.close()
        self = LoadMenu(self.geometry())
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoadMenu()
    sys.exit(app.exec())