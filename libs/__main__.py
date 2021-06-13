from PyQt5 import QtWidgets
import sys
from .app_window import AppWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = AppWindow()
    main_window.show()
    sys.exit(app.exec_())
