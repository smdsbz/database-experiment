# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/admin-window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(557, 418)
        font = QtGui.QFont()
        font.setFamily("宋体")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.tabwidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabwidget.sizePolicy().hasHeightForWidth())
        self.tabwidget.setSizePolicy(sizePolicy)
        self.tabwidget.setMinimumSize(QtCore.QSize(480, 360))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.tabwidget.setFont(font)
        self.tabwidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabwidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabwidget.setObjectName("tabwidget")
        self.merchtab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.merchtab.sizePolicy().hasHeightForWidth())
        self.merchtab.setSizePolicy(sizePolicy)
        self.merchtab.setMinimumSize(QtCore.QSize(0, 0))
        self.merchtab.setObjectName("merchtab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.merchtab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.merch_table = QtWidgets.QTableWidget(self.merchtab)
        self.merch_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.merch_table.setObjectName("merch_table")
        self.merch_table.setColumnCount(4)
        self.merch_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        item.setFont(font)
        self.merch_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        item.setFont(font)
        self.merch_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        item.setFont(font)
        self.merch_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        item.setFont(font)
        self.merch_table.setHorizontalHeaderItem(3, item)
        self.merch_table.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.merch_table, 0, 0, 1, 1)
        self.tabwidget.addTab(self.merchtab, "")
        self.employeetab = QtWidgets.QWidget()
        self.employeetab.setObjectName("employeetab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.employeetab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabwidget.addTab(self.employeetab, "")
        self.transtab = QtWidgets.QWidget()
        self.transtab.setObjectName("transtab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.transtab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabwidget.addTab(self.transtab, "")
        self.gridLayout.addWidget(self.tabwidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 557, 18))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.file_menu.setFont(font)
        self.file_menu.setObjectName("file_menu")
        self.refresh_menu = QtWidgets.QMenu(self.file_menu)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.refresh_menu.setFont(font)
        self.refresh_menu.setObjectName("refresh_menu")
        self.help_menu = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.help_menu.setFont(font)
        self.help_menu.setObjectName("help_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.about_action = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.about_action.setFont(font)
        self.about_action.setObjectName("about_action")
        self.exit_action = QtWidgets.QAction(MainWindow)
        self.exit_action.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.exit_action.setFont(font)
        self.exit_action.setIconVisibleInMenu(True)
        self.exit_action.setObjectName("exit_action")
        self.refresh_merch_action = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.refresh_merch_action.setFont(font)
        self.refresh_merch_action.setObjectName("refresh_merch_action")
        self.refresh_employee_action = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.refresh_employee_action.setFont(font)
        self.refresh_employee_action.setObjectName("refresh_employee_action")
        self.refresh_trans_action = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.refresh_trans_action.setFont(font)
        self.refresh_trans_action.setObjectName("refresh_trans_action")
        self.refresh_all_action = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.refresh_all_action.setFont(font)
        self.refresh_all_action.setObjectName("refresh_all_action")
        self.refresh_menu.addAction(self.refresh_merch_action)
        self.refresh_menu.addAction(self.refresh_employee_action)
        self.refresh_menu.addAction(self.refresh_trans_action)
        self.refresh_menu.addSeparator()
        self.refresh_menu.addAction(self.refresh_all_action)
        self.file_menu.addAction(self.refresh_menu.menuAction())
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
        self.help_menu.addAction(self.about_action)
        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.help_menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabwidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "管理员客户端"))
        item = self.merch_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "商品 ID"))
        item = self.merch_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "商品名称"))
        item = self.merch_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "单价"))
        item = self.merch_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "库存"))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.merchtab), _translate("MainWindow", "商品信息"))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.employeetab), _translate("MainWindow", "店员信息"))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.transtab), _translate("MainWindow", "交易信息"))
        self.file_menu.setTitle(_translate("MainWindow", "文件"))
        self.refresh_menu.setTitle(_translate("MainWindow", "刷新"))
        self.help_menu.setTitle(_translate("MainWindow", "帮助"))
        self.about_action.setText(_translate("MainWindow", "关于"))
        self.exit_action.setText(_translate("MainWindow", "退出"))
        self.refresh_merch_action.setText(_translate("MainWindow", "刷新商品列表"))
        self.refresh_employee_action.setText(_translate("MainWindow", "刷新店员信息"))
        self.refresh_trans_action.setText(_translate("MainWindow", "刷新交易信息"))
        self.refresh_all_action.setText(_translate("MainWindow", "全部刷新"))
