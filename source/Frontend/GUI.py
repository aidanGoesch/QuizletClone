# main script for the GUI/frontend
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QPushButton, QGridLayout, QWidget, QLabel, QGraphicsOpacityEffect
from PyQt6.QtGui import QAction, QFont, QEnterEvent, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation
from source.Frontend.Editor.editor import Editor
from source.Frontend.Editor.load_menu import LoadMenu
from source.Backend.Log.logging import reset_log

class MainWindow(QMainWindow):
    def __init__(self, geometry = None):
        super().__init__()
        self.initUI(geometry)

    def initUI(self, geometry):
        w = QWidget()
        self.setCentralWidget(w)

        # Create a layout for the scrollable widget
        layout = QGridLayout(w)

        title = QLabel(text="Fake Quizlet")
        title.setFont(QFont('Times', 40))
        title.setStyleSheet("color: white;")
        title.setMinimumHeight(20)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, 0, 0, 1, 2)

        new_button = QPushButton(text="New Study Set")
        new_button.setFont(QFont('Times', 20))
        new_button.setMinimumHeight(70)
        new_button.clicked.connect(lambda : self.open_editor())
        layout.addWidget(new_button, 1, 0, 1, 1)

        open_button = QPushButton(text="Open Study Set")
        open_button.setFont(QFont('Times', 20))
        open_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                  "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                   "QPushButton:hover { border-color: white; }")

        open_button.setMinimumHeight(70)
        open_button.clicked.connect(lambda : self.open_load_menu())
        layout.addWidget(open_button, 1, 1, 1, 1)

        blank_space = QWidget()
        layout.addWidget(blank_space, 2, 0, 1, 2)

        self.setWindowTitle("Main Menu Example")
        if geometry is None:
            self.setGeometry(200, 200, 700, 500)
        else:
            self.setGeometry(geometry)

        self.setStyleSheet("background-color: rgb(28, 44, 37);")
        self.show()

    def open_editor(self):
        self.editor_window = Editor(self.geometry())
        self.editor_window.show()
        self.close()

    def open_load_menu(self):
        self.load_menu = LoadMenu(self.geometry())
        self.load_menu.show()
        self.close()


def main():
    reset_log()
    app = QApplication(sys.argv)
    window = LoadMenu()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()