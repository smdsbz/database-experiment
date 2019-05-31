# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/login-window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 140)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(240, 140))
        Dialog.setMaximumSize(QtCore.QSize(240, 140))
        font = QtGui.QFont()
        font.setFamily("宋体")
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.user_label = QtWidgets.QLabel(Dialog)
        self.user_label.setObjectName("user_label")
        self.gridLayout.addWidget(self.user_label, 0, 0, 1, 1)
        self.passwd_label = QtWidgets.QLabel(Dialog)
        self.passwd_label.setObjectName("passwd_label")
        self.gridLayout.addWidget(self.passwd_label, 2, 0, 1, 1)
        self.login_button = QtWidgets.QPushButton(Dialog)
        self.login_button.setObjectName("login_button")
        self.gridLayout.addWidget(self.login_button, 4, 3, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 4, 4, 1, 1)
        self.passwd_input = QtWidgets.QLineEdit(Dialog)
        self.passwd_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwd_input.setObjectName("passwd_input")
        self.gridLayout.addWidget(self.passwd_input, 2, 1, 1, 4)
        self.user_input = QtWidgets.QLineEdit(Dialog)
        self.user_input.setObjectName("user_input")
        self.gridLayout.addWidget(self.user_input, 0, 1, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.user_input, self.passwd_input)
        Dialog.setTabOrder(self.passwd_input, self.login_button)
        Dialog.setTabOrder(self.login_button, self.cancel_button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "登陆"))
        self.user_label.setText(_translate("Dialog", " 用户名 "))
        self.passwd_label.setText(_translate("Dialog", " 密  码 "))
        self.login_button.setText(_translate("Dialog", "登陆"))
        self.cancel_button.setText(_translate("Dialog", "退出"))

