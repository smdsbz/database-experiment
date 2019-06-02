# -*- coding: utf-8 -*-

import toml
from PyQt5 import QtCore, QtWidgets

CONFIG = toml.load('config/client.toml')

def qmessage_critical_with_detail(title: str, info: str, detail: str, parent=None):
    warn = QtWidgets.QMessageBox(
        QtWidgets.QMessageBox.Critical, title, info,
        buttons=QtWidgets.QMessageBox.Ok, parent=parent
    )
    warn.setDetailedText(detail)
    return warn.exec_()


from .LoginWindow import LoginWindow
from .AdminWindow import AdminWindow
from .SellerWindow import SellerWindow

__all__ = [
    'CONFIG',
    'qmessage_critical_with_detail',
    'LoginWindow'
]
