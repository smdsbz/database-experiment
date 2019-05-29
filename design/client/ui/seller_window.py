# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/seller-window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(498, 414)
        font = QtGui.QFont()
        font.setFamily("宋体")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabwidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabwidget.setMinimumSize(QtCore.QSize(480, 360))
        self.tabwidget.setObjectName("tabwidget")
        self.transtab = QtWidgets.QWidget()
        self.transtab.setObjectName("transtab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.transtab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)
        self.is_vip_checkbox = QtWidgets.QCheckBox(self.transtab)
        self.is_vip_checkbox.setObjectName("is_vip_checkbox")
        self.gridLayout_2.addWidget(self.is_vip_checkbox, 1, 0, 1, 1)
        self.trans_table = QtWidgets.QTableWidget(self.transtab)
        self.trans_table.setObjectName("trans_table")
        self.trans_table.setColumnCount(4)
        self.trans_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        item.setFont(font)
        self.trans_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        item.setFont(font)
        self.trans_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        item.setFont(font)
        self.trans_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        item.setFont(font)
        self.trans_table.setHorizontalHeaderItem(3, item)
        self.gridLayout_2.addWidget(self.trans_table, 0, 0, 1, 5)
        self.add_item_button = QtWidgets.QPushButton(self.transtab)
        self.add_item_button.setObjectName("add_item_button")
        self.gridLayout_2.addWidget(self.add_item_button, 1, 2, 1, 1)
        self.remove_selected_button = QtWidgets.QPushButton(self.transtab)
        self.remove_selected_button.setObjectName("remove_selected_button")
        self.gridLayout_2.addWidget(self.remove_selected_button, 1, 3, 1, 1)
        self.clear_button = QtWidgets.QPushButton(self.transtab)
        self.clear_button.setObjectName("clear_button")
        self.gridLayout_2.addWidget(self.clear_button, 2, 3, 1, 1)
        self.submit_uutton = QtWidgets.QPushButton(self.transtab)
        self.submit_uutton.setObjectName("submit_uutton")
        self.gridLayout_2.addWidget(self.submit_uutton, 2, 2, 1, 1)
        self.tabwidget.addTab(self.transtab, "")
        self.viptab = QtWidgets.QWidget()
        self.viptab.setObjectName("viptab")
        self.tabwidget.addTab(self.viptab, "")
        self.gridLayout.addWidget(self.tabwidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 498, 18))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.menu.setFont(font)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.action.setFont(font)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabwidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.is_vip_checkbox.setText(_translate("MainWindow", "是否会员"))
        item = self.trans_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "商品 ID"))
        item = self.trans_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "商品名称"))
        item = self.trans_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "折后单价"))
        item = self.trans_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "库存"))
        self.add_item_button.setText(_translate("MainWindow", "添加"))
        self.remove_selected_button.setText(_translate("MainWindow", "删除选中项"))
        self.clear_button.setText(_translate("MainWindow", "全部清空"))
        self.submit_uutton.setText(_translate("MainWindow", "提交订单"))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.transtab), _translate("MainWindow", "收银页面"))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.viptab), _translate("MainWindow", "会员注册"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.action.setText(_translate("MainWindow", "退出"))

