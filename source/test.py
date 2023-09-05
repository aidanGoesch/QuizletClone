# import sys
#
# from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QRadioButton, QPushButton
# from PyQt6.QtCore import Qt
#
# # Create an instance of QApplication
# app = QApplication(sys.argv)
#
#
# # 3. Create your application's GUI
# window = QWidget()
# window.setWindowTitle("PyQt App")
# window.setGeometry(100, 100, 280, 80)
#
# # # This is how you display text onto the window
# # helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
# # helloMsg.move(60, 15)
#
#
# # # This is how you get whatever is in the text box
# # def print_text():
# #     print(test.text())
# #
# # test = QLineEdit(parent=window) # parent is what associates it with the window
# # test.returnPressed.connect(print_text)
# # test.move(60, 15)
#
# # def print_dick(button):
# #     if button.isChecked():
# #         print('dick')
# #
# # test_button_1 = QRadioButton(parent=window)
# # test_button_1.setText("Fuck")
# # test_button_1.move(10, 0)
# #
# # test_button_2 = QRadioButton(parent=window)
# # test_button_2.setText("Shit")
# # test_button_2.move(10, 20)
# #
# # test_button_3 = QRadioButton(parent=window)
# # test_button_3.setText("Dick")
# # test_button_3.move(10, 40)
# #
# # test_button_3.toggled.connect(lambda: print_dick(test_button_3))
# # connect takes a lambda function that doesn't take any args and in the lambda function you
# # can call other normal functions and pass in the specific button
#
#
# def the_button_was_clicked():
#     if test.isChecked():
#         if test.text() == "poo":
#             test.setText("something")
#         else:
#             test.setText("poo")
#
#         test.setChecked(False)
#         print("Clicked!")
#
#
# test = QPushButton(text='something',parent=window)
# test.setCheckable(False)  # makes it so that you can track whether the button has been clicked
#
# test.clicked.connect(the_button_was_clicked)
#
# test.resize(100, 100)
# test.move(60, 15)


from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect

if __name__ == "__main__":
    app = QApplication([])

    window = QMainWindow()
    window.setWindowTitle("Main Window")
    window.setGeometry(100, 100, 500, 400)

    button = QPushButton("Hover Me")
    button.setStyleSheet(
        "QPushButton { border: 2px solid transparent; border-radius: 5px; }"
        "QPushButton:hover { border: 2px solid white; }"
    )
    button.setProperty("hovered", False)

    animation = QPropertyAnimation(button, b"styleSheet")
    animation.setDuration(200)
    animation.setStartValue(button.styleSheet())
    animation.setEndValue(button.styleSheet().replace("transparent", "white"))

    def start_animation(event):
        if not button.property("hovered"):
            button.setProperty("hovered", True)
            button.style().unpolish(button)
            button.style().polish(button)
            animation.start()

    def reset_animation(event):
        if button.property("hovered"):
            button.setProperty("hovered", False)
            button.style().unpolish(button)
            button.style().polish(button)
            animation.start()

    button.enterEvent = start_animation
    button.leaveEvent = reset_animation

    window.setCentralWidget(button)

    window.show()

    app.exec()

#
#
#
#
# # 4. Show your application's GUI
# window.show()
#
# # 5. Run your application's event loop
# sys.exit(app.exec())
#
#
#
# # Notes
#
# # QPushButton is a button (usually yes, no, close, or cancel)
#
# # QLineEdit is a text box
#
# # QComboBox is a drop down box that lets you pick from a pool of options
#
# # QRadioButton is a button where when you select a different option
# #                   it deselects the previosuly selected option