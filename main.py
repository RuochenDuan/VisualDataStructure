# main.py
import sys
from PyQt6.QtWidgets import QApplication
from views import Window
from controllers import MainController
from config import GSS


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(GSS)
    window = Window()
    main_controller = MainController(window)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
