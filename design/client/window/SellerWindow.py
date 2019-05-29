# -*- coding: utf-8 -*-

from PyQt5 import QtCore as C
from PyQt5 import QtGui as G
from PyQt5 import QtWidgets as W
import requests

from . import CONFIG, qmessage_critical_with_detail
from ui import Ui_SellerWindow


class SellerWindow(W.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_SellerWindow()
        self.ui.setupUi()

        self.user_data = {}
