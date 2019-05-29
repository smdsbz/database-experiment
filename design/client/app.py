# -*- coding: utf-8 -*-

import sys
import PyQt5 as Q
from PyQt5 import uic, QtWidgets as W

from window import LoginWindow


if __name__ == '__main__':
    app = W.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
