# -*- coding: utf-8 -*-

import sys
import PyQt5 as Q

from window import LoginWindow


if __name__ == '__main__':
    app = Q.QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    try:
        sys.exit(app.exec())
    except Exception as e:
        window.next_window.close()
