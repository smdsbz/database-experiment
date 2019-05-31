# -*- coding: utf-8 -*-

import hashlib

from PyQt5 import QtWidgets as W
import requests

from . import CONFIG, qmessage_critical_with_detail
from .AdminWindow import AdminWindow
from .SellerWindow import SellerWindow
from ui import Ui_LoginWindow

URL = CONFIG['remote']['url']


class LoginWindow(W.QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        # register slot functions
        self.ui.login_button.clicked.connect(self.handle_login_button_clicked)
        self.ui.cancel_button.clicked.connect(self.handle_cancel_button_clicked)

    # NOTE DO NOT use names on_[object_name]_[signal_name] for slots!!!
    #      You may override the original slot functions!

    def handle_login_button_clicked(self):
        user, passwd = (
            self.ui.user_input.text(),
            hashlib.md5(self.ui.passwd_input.text().encode('utf-8')).hexdigest()
        )
        try:
            ret = requests.get(f'{URL}/api/auth/login/{user}/{passwd}')
        except Exception as e:
            qmessage_critical_with_detail('连接错误', '无法连接至服务端！', str(e), self)
            return
        if ret.status_code != 200:
            if ret.status_code == 406:
                msg = ret.json()
                if msg == 'User not found':
                    msg = '用户名不存在！'
                elif msg == 'Wrong password':
                    msg = '密码错误！'
                elif msg == 'User already logged-in elsewhere':
                    msg = '用户已在其他地方登陆！'
                ret = W.QMessageBox.warning(self, '警告', msg)
                return
            ret = W.QMessageBox.critical(self, '错误', '发生了未知的服务端错误！')
            return
        ret = ret.json()
        if ('employee_id' not in ret) or ('role' not in ret):
            ret = W.QMessageBox.critical(self, '错误', '服务端通信协议升级，请更新您的客户端！')
            return
        employee_id, role = ret['employee_id'], ret['role']
        print(f'Successfully logged-in as {user} ({employee_id}, {role})!')
        if role == 'admin':
            self.next_window = AdminWindow()
        elif role == 'common':
            self.next_window = SellerWindow()
        else:
            raise ValueError(f'Window for role {role} not implemented!')
        self.next_window.user_data['login'] = user
        self.next_window.user_data['employee_id'] = employee_id
        self.next_window.user_data['role'] = role
        self.next_window.user_data['auth'] = (user, passwd)
        self.next_window.show()
        self.close()

    def handle_cancel_button_clicked(self):
        self.close()

    def closeEvent(self, evt):
        return super().closeEvent(evt)
