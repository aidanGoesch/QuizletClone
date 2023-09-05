import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QScrollArea, QPushButton, QGridLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal
from source.Backend.Log.logging import log

class DeleteDialogue(QMainWindow):
    deleted = pyqtSignal()
    def __init__(self, geometry=None, file_name=None):
        super().__init__()
        self.file_name = file_name
        self.setGeometry(200, 200, 700, 500)
        self.setFixedSize(350, 175)
        self.setWindowTitle(" ")

        if geometry is not None:
            center = geometry.center()
            x = center.x() - self.width() // 2
            y = center.y() - self.height() // 2
            self.move(x, y)

        self.geometry().topLeft().setX(int(x * 1.5))
        self.geometry().topLeft().setY(int(y * 1.5))

        self.setStyleSheet("background-color: rgb(28, 44, 37);")

        w = QWidget()
        self.setCentralWidget(w)

        self.layout = QGridLayout(w)

        query = QLabel("Are you sure you want to delete this set?")
        query.setMinimumHeight(40)
        query.setFont(QFont('Times', 13))
        query.setStyleSheet("color: white;")
        query.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(query, 0, 0, 1, 2)

        yes_button = QPushButton("delete set")
        yes_button.setMinimumHeight(40)
        yes_button.setFont(QFont('Times', 13))
        yes_button.clicked.connect(lambda: self.delete_set())
        yes_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                     "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                     "QPushButton:hover { border-color: white; }")

        self.layout.addWidget(yes_button, 1, 0, 1, 1)

        yes_button = QPushButton("don't delete")
        yes_button.setMinimumHeight(40)
        yes_button.setFont(QFont('Times', 13))
        yes_button.clicked.connect(self.close)
        yes_button.setStyleSheet("QPushButton { border: 3px solid transparent;"
                                 "color: white; background-color: rgb(73, 91, 85); border-radius: 10px; }"
                                 "QPushButton:hover { border-color: white; }")

        self.layout.addWidget(yes_button, 1, 1, 1, 1)

        self.show()

    def delete_set(self):
        from source.Backend.file_handler import delete_set
        x = delete_set(self.file_name)
        if not x:
            log(f'something went wrong, {self.file_name} could not be deleted')
        else:
            self.deleted.emit()
            log('Set deleted successfully')

        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DeleteDialogue()
    sys.exit(app.exec())
